from . import db
from . import models


def get_notifications(email=None):
    '''
    Название 	Скидка 	Дата поиска 	Отправка уведомления 	Код товара
    Product.name Query.discount Notification.created_at  Product.id

    '''
    notifications = models.Notification.query.all()
    notification_data = []
    for notification in notifications:
        product_name = notification.product.name
        discount = notification.query.discount
        created_at = notification.created_at
        product_id = notification.product.id

        # Добавляем данные уведомления в список
        notification_data.append((product_name, discount, created_at, product_id))

    if email:
        user = models.User.query.filter_by(email=email).first()
        if user:
            for query in user.queries:
                for notification in query.notifications:
                    product_name = notification.product.name
                    discount = notification.query.discount
                    created_at = notification.created_at
                    product_id = notification.product.id

                    # Добавляем данные уведомления в список
                    notification_data.append((product_name, discount, created_at, product_id))

    return notification_data


def add_query_to_database(username, email, query, discount):
    user = models.User.query.filter_by(email=email).first()

    if not user:
        # Создаем нового пользователя, если адрес электронной почты не существует
        user = models.User(name=username, email=email)
        db.session.add(user)
        db.session.commit()

    new_query = models.Query(user_id=user.id, query_title=query, discount=discount)
    db.session.add(new_query)
    db.session.commit()


def add_product_history_data(product_id, product_name, current_price, query_obj):
    product = models.Product.query.filter_by(id=product_id).first()
    if not product:
        # Создаем новый продукт, если он не существует
        product = models.Product(id=product_id, name=product_name, price=current_price)
        db.session.add(product)
        db.session.commit()
        return

    # Добавляем данные продукта в таблицу истории
    history_entry = models.History(product_id=product.id, price=current_price)
    db.session.add(history_entry)
    db.session.commit()
    discount = query_obj.discount
    initial_price = product.price

    if current_price < initial_price - (initial_price * (discount / 100)):
        # Записываем уведомление, если текущая цена ниже с учетом скидки
        notification = models.Notification(
            product=product,
            query=query_obj,
            previous_price=initial_price,
            current_price=current_price
        )
        db.session.add(notification)
        db.session.commit()
        email = query_obj.user.email
        return (query_obj.query_title, product_name, discount, current_price, product_id, email)
    return
