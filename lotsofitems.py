from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, Category, Item

engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

user1 = User(id=1, name="Tom")

# Test Category Data
category1 = Category(id=1, name="Skiing")
session.add(category1)
session.commit()

category2 = Category(id=2, name="Basketball")
session.add(category2)
session.commit()

category3 = Category(id=3, name="Tennis")
session.add(category3)
session.commit()

category4 = Category(id=4, name="Golf")
session.add(category4)
session.commit()

category5 = Category(id=5, name="Baseball")
session.add(category5)
session.commit()

category6 = Category(id=6, name="Hockey")
session.add(category6)
session.commit()

category7 = Category(id=7, name="Soccer")
session.add(category7)
session.commit()

category8 = Category(id=8, name="Pool")
session.add(category8)
session.commit()

# Test Item Data
item1 = Item(id=1, name="Skis", description="These are long boards that attach to your feet, allowing you to slide down a snowy hill.",
                     category_id=1, user_id=1)
session.add(item1)
session.commit()


item2 = Item(id=2, name="Poles", description="Poles are sticks that assist you in sliding down a hill.",
                     category_id=1, user_id=1)
session.add(item2)
session.commit()

item3 = Item(id=3, name="Gloves", description="You wear them on your hands.",
                     category_id=1, user_id=1)
session.add(item3)
session.commit()

item4 = Item(id=4, name="Shoes", description="Great for jumping and running and stuff.",
                     category_id=2, user_id=1)
session.add(item4)
session.commit()

item5 = Item(id=5, name="Basketball", description="Use this ball to play basketball.",
                     category_id=2, user_id=1)
session.add(item5)
session.commit()

item6 = Item(id=6, name="Headband", description="It will keep that sweat out of your eyes, dog.",
                     category_id=2, user_id=1)
session.add(item6)
session.commit()

item7 = Item(id=7, name="Racket", description="Hit those balls with this thing.",
                     category_id=3, user_id=1)
session.add(item7)
session.commit()

item8 = Item(id=8, name="Tennis Balls", description="These get hit over the net and whatnot.",
                     category_id=3, user_id=1)
session.add(item8)
session.commit()

item9 = Item(id=9, name="Tennis Bag", description="Keep all of your tennis stuff in this guy.",
                     category_id=3, user_id=1)
session.add(item9)
session.commit()

item10 = Item(id=10, name="Golf Club", description="Use this to hit those golf balls.",
                     category_id=4, user_id=1)
session.add(item10)
session.commit()

item11 = Item(id=11, name="Golf Bag", description="Keep all your clubs and balls in this thing.",
                     category_id=4, user_id=1)
session.add(item11)
session.commit()

item12 = Item(id=12, name="Golf Balls", description="Hit these little guys with your golf clubs.",
                     category_id=4, user_id=1)
session.add(item12)
session.commit()

item13 = Item(id=13, name="Baseball Bat", description="Knock it over the fence or whatever.",
                     category_id=5, user_id=1)
session.add(item13)
session.commit()

item14 = Item(id=14, name="Baseball Glove", description="Catch all sorts of things with this.",
                     category_id=5, user_id=1)
session.add(item14)
session.commit()

item15 = Item(id=15, name="Baseballs", description="Go ahead and hit these guys.",
                     category_id=5, user_id=1)
session.add(item15)
session.commit()

item16 = Item(id=16, name="Hockey Stick", description="Take slap shots or whatever.",
                     category_id=6, user_id=1)
session.add(item16)
session.commit()

item17 = Item(id=17, name="Hockey Puck", description="This is not a biscuit.",
                     category_id=6, user_id=1)
session.add(item17)
session.commit()

item18 = Item(id=18, name="Ice Skates", description="Slide all over the place with these guys on your feet.",
                     category_id=6, user_id=1)
session.add(item18)
session.commit()

item19 = Item(id=19, name="Soccer Ball", description="Kick this guy around.",
                     category_id=7, user_id=1)
session.add(item19)
session.commit()

item20 = Item(id=20, name="Soccer Uniform", description="Because who plays soccer in a regular shirt?",
                     category_id=7, user_id=1)
session.add(item20)
session.commit()

item21 = Item(id=21, name="Cleats", description="Stop slipping and sliding all over the place.",
                     category_id=7, user_id=1)
session.add(item21)
session.commit()

item22 = Item(id=22, name="Pool Cue", description="Great for 8 ball and musical gang fights.",
                     category_id=8, user_id=1)
session.add(item22)
session.commit()

item23 = Item(id=23, name="Pool Balls", description="There's 16 of them and they are real hard.",
                     category_id=8, user_id=1)
session.add(item23)
session.commit()

item24 = Item(id=24, name="Pool Table", description="Good luck taking this home on the subway.",
                     category_id=8, user_id=1)
session.add(item24)
session.commit()
