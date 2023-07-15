import { useState, useEffect, forwardRef } from 'react';
import {
    Card,
    Table,
    TableHead,
    TableBody,
    TableRow,
    TableCell,
    TablePagination,
    Typography,
    Modal,
    Button,
    Box,
    TextField,
    Stack,
    Snackbar,
} from '@mui/material';
import MuiAlert, { AlertProps } from '@mui/material/Alert';

const style = {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: 500,
    bgcolor: 'background.paper',
    border: '2px solid #000',
    boxShadow: 24,
    p: 4,
};

const Alert = forwardRef(function Alert(props, ref) {
    return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
  });
  

const Comments = () => {
    const [commentList, setCommentList] = useState([]);
    const [commentCount, setCommentCount] = useState(0);
    const [controller, setController] = useState({
        page: 0,
        rowsPerPage: 10
    });
    const [open, setOpen] = useState(false);
    const [openSnackbar, setOpenSnackbar] = useState(false);
    const [currentcomment, setCurrentComment] = useState({})
    const [report, setReport] = useState('');
    const handleOpen = () => setOpen(true);
    const handleClose = () => setOpen(false);
    const handleCloseSnackbar = () => setOpenSnackbar(false);

    useEffect(() => {
        const getData = async () => {
            const skip = controller.page * controller.rowsPerPage;
            let auth = localStorage.getItem('tokens');
            const url = `http://localhost/api/comment-mismatch-prediction/skip/${skip}/limit/${controller.rowsPerPage}`
            try {
                const response = await fetch(url, {
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': "Bearer " + auth,
                    }
                });
                if (response.statusText === 'OK') {
                    const res = await response.json();
                    console.log(res.data);
                    setCommentList(res.data);
                    setCommentCount(res.total);
                } else {
                    throw new Error('Request failed')
                }
            } catch (error) {
                console.log(error);
            }
        };
        getData();
    }, [controller]);

    const handlePageChange = (event, newPage) => {
        setController({
            ...controller,
            page: newPage
        });
    };

    const handleChangeRowsPerPage = (event) => {
        setController({
            ...controller,
            rowsPerPage: parseInt(event.target.value, 10),
            page: 0
        });
    };

    const handleModalDisagree = async (cmt) => {
        handleOpen();
        setCurrentComment(cmt);   
    }

    const handleAgree = async (cmt) => {
        handleConfirmResult(cmt.id, cmt.model_prediction, '')
        setOpenSnackbar(true);
    }

    const updateNoWithReport = async () => {
        let confirm_result = currentcomment.model_prediction == 'NEG' ? 'POS' : 'NEG';
        handleConfirmResult(currentcomment.id, confirm_result, report);
        handleClose();
        setOpenSnackbar(true);
    }

    const handleConfirmResult = async (id, confirmation, report) => {
        const skip = controller.page * controller.rowsPerPage;
        let auth = localStorage.getItem('tokens');
        let payload = {
            id: id,
            verified_result: confirmation,
            report_comment: report
        }
        const url = `http://localhost/api/comment/review`
        try {
            const response = await fetch(url, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': "Bearer " + auth,
                },
                body: JSON.stringify(payload),
                method: 'POST'
            });
            if (response.statusText === 'OK') {
                console.log('Updae success')
                setController({
                    ...controller,
                    rowsPerPage: controller.rowsPerPage,
                    page: controller.page
                });
            } else {
                throw new Error('Request failed')
            }
        } catch (error) {
            console.log(error);
        }
    }

    return (
        <div>
            <Card>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>
                                Content
                            </TableCell>
                            <TableCell>
                                Prediction
                            </TableCell>
                            <TableCell>
                                Rating
                            </TableCell>
                            <TableCell>
                                Action
                            </TableCell>
                            <TableCell>
                            </TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {commentList.map((comment) => (
                            <TableRow key={comment.id}>
                                <TableCell>
                                    <a href={"https://www.foody.vn" + comment.url}>{comment.url}</a><br></br><br></br>
                                    {comment.content}
                                </TableCell>
                                <TableCell>
                                    {comment.model_prediction}
                                </TableCell>
                                <TableCell>
                                    {comment.rating}
                                </TableCell>
                                <TableCell>
                                    <Button type="button" onClick={() => handleAgree(comment)}>Yes</Button>
                                </TableCell>
                                <TableCell>
                                    <Button type="button" onClick={() => handleModalDisagree(comment)}>No</Button>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
                <TablePagination
                    component="div"
                    onPageChange={handlePageChange}
                    page={controller.page}
                    count={commentCount}
                    rowsPerPage={controller.rowsPerPage}
                    onRowsPerPageChange={handleChangeRowsPerPage}
                />
            </Card>
            <Modal
                open={open}
                onClose={handleClose}
                aria-labelledby="modal-modal-title"
                aria-describedby="modal-modal-description"
            >
                <Box sx={style}>
                    <Typography id="modal-modal-title" variant="h6" component="h2">
                        Report to Foody
                    </Typography>
                    <TextField id="text_comment" label="Content" variant="filled" fullWidth
                        onChange={event => setReport(event.target.value)} />
                    <Button type="button" onClick={() => updateNoWithReport()}>Send</Button>
                </Box>
            </Modal>
            <Stack spacing={2} sx={{ width: '100%' }}>
                <Snackbar open={openSnackbar} autoHideDuration={6000} onClose={handleCloseSnackbar}>
                    <Alert onClose={handleClose} severity="success" sx={{ width: '100%' }}>
                        Update successfully!
                    </Alert>
                </Snackbar>
            </Stack>
        </div>
    )
}

export default Comments;