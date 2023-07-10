import torch
from transformers import RobertaForSequenceClassification, AutoTokenizer

model = RobertaForSequenceClassification.from_pretrained("./phobert-base-vietnamese-sentiment")

tokenizer = AutoTokenizer.from_pretrained("./phobert-base-vietnamese-sentiment", use_fast=False)

# Just like PhoBERT: INPUT TEXT MUST BE ALREADY WORD-SEGMENTED!
sentence = "Sao có thể có chỗ vừa NGON, VỪA RẺ NHƯ VẬY CHỨ! NƯỚC DÙNG VỊ VỪA PHẢI KO GẮT KO NHẠT, NHIỀU THỊT, CHU ĐÁO ĐẾN TỪNG BỊCH SA TẾ, BỊCH CHANH, TỪNG BỊCH BÚN VÀ TÔ ĂN ĐỂ RIÊNG RẤT GỌN GÀNG"  

input_ids = torch.tensor([tokenizer.encode(sentence)])

with torch.no_grad():
    out = model(input_ids)
    output = out.logits.softmax(dim=-1).tolist()[0]
    label = ['NEG', 'POS', 'NEU']
    print(label[output.index(max(output))])
    
    print(out.logits.softmax(dim=-1).tolist())
    # Output:
    # [[0.002, 0.988, 0.01]]
    #     ^      ^      ^
    #    NEG    POS    NEU
