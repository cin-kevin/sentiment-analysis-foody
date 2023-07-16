import logging

from shared.db import engine
from shared.db.schemas import Comment, Restaurant, User
from shared.utils import get_uuid
from sqlalchemy.orm import sessionmaker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init(engine_in):
    engine_ = engine_in
    if not engine_:
        engine_ = engine
    dbsession = sessionmaker(autocommit=False, autoflush=False, bind=engine_)
    
    with dbsession() as session:
        user = session.query(User).filter(User.username == "CTV").first()

        if not user:
            user_in = User(id=1, username="CTV", password="password1")
            session.add(user_in)
            session.commit()

        restaurant = (
            session.query(Restaurant)
            .filter(
                Restaurant.url
                == "https://www.foody.vn/ho-chi-minh/bun-bo-vuong-674-thong-nhat"
            )
            .first()
        )

        if not restaurant:
            restaurant_in = Restaurant(
                id=1,
                name="Bún Bò Vuông",
                address="674 Thống Nhất, P. 15,  Quận Gò Vấp, TP. HCM",
                url="https://www.foody.vn/ho-chi-minh/bun-bo-vuong-674-thong-nhat",
            )
            session.add(restaurant_in)
            session.commit()

        contents = [
            (
                "Sao có thể có chỗ vừa NGON, VỪA RẺ NHƯ VẬY CHỨ! NƯỚC DÙNG VỊ VỪA PHẢI KO GẮT KO NHẠT, NHIỀU THỊT, CHU ĐÁO ĐẾN TỪNG BỊCH SA TẾ, BỊCH CHANH, TỪNG BỊCH BÚN VÀ TÔ ĂN ĐỂ RIÊNG RẤT GỌN GÀNG",
                10,
            ),
            (
                "Đôi khi nước dùng hay bị nhạt nhẽo. Nhất là nếu mua vào lúc sớm. Nạm bò có hôm mềm có hôm hơi dai. Được cái phục vụ nhiệt tình. Ăn chống đói đêm khuya",
                7,
            ),
            (
                "Đặt 2 lần tiếp theo ở chi nhánh này. 1 lần là tô đặt biệt có thịt nạm với khoanh giò, ko có miếng chả nào cả và 1 bịch nước lèo thịt tái. Lần sau đặt tô đầy đủ thêm chả cua. (Ko đặt đc chả quế chứ chả cua ăn chán lắm) cả 2 lần đều xin nhiều ớt nhưng lát đát vài lát ớt, ăn ko đã. Ko đặt chi nhánh này nữa.",
                6,
            ),
        ]

        comment = session.query(Comment).first()

        if not comment:
            cid = 1
            for content in contents:
                comment_in = Comment(
                    id=cid,
                    content=content[0],
                    rating=content[1],
                    need_review=False,
                    restaurant_id=restaurant_in.id,
                )
                session.add(comment_in)
                session.commit()
                cid += 1


def main():
    logger.info("Creating intial data...")
    init()
    logger.info("Initiala data created")


if __name__ == "__main__":
    main()
