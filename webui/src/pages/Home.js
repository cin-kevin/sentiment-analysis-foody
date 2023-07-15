import Card from "react-bootstrap/Card";
import Comments from "../components/Comments";
import AuthContext from "../components/shared/AuthContext";
import { Link } from "react-router-dom";
import { useContext } from "react";
const Home = () => {
  const { user, logout } = useContext(AuthContext);
  return (
    <>
      <div
        className="d-flex justify-content-center align-items-center"
        style={{ minHeight: "500px", minWidth: "600px" }}
      >
        <Card>
          <Card.Body>
            <Card.Text className="text-center">
              <b>Unmatched rating with model prediction</b>
            </Card.Text>
            {user && (<Comments></Comments>)}
          </Card.Body>
        </Card>
      </div>
    </>
  );
};

export default Home;
