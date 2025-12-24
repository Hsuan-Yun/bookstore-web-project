from django.db import models

#會員資料
class Member(models.Model):
    member_id = models.AutoField(primary_key=True)
    memberName = models.CharField(max_length=50)
    memberAccount = models.CharField(max_length=50, unique=True)
    memberPassword = models.CharField(max_length=30)
    memberBirthday = models.DateField()
    memberAge = models.IntegerField(default=0)
    memberEmail = models.EmailField()
    memberAddress = models.CharField(max_length=200, null=True)
    memberPhone = models.CharField(max_length=15, null=True)
    memberPoint = models.IntegerField(default=105)
    memberTotalAmount = models.IntegerField(default=0)
    
    def __str__(self):
        return self.memberName

#書籍資料
class Product(models.Model):
    product_id = models.IntegerField(primary_key=True, db_index=True)
    productName = models.CharField(max_length=50)
    author_id = models.IntegerField(db_index=True)
    publisher_id = models.IntegerField(db_index=True)
    productCategory = models.CharField(max_length=50)
    productPrice = models.IntegerField(default=0)
    productStock = models.IntegerField(default=0)
    productLanguage = models.CharField(max_length=10)
    productPublishDate = models.DateField()
    productIntroduce = models.TextField(max_length=1000)
    productSold = models.IntegerField(default=0)
    productAgeLimit = models.IntegerField(default=0)

    def __str__(self):
        return self.productName

#書籍封面路徑
class Images(models.Model):
    images_id = models.IntegerField(primary_key=True)
    product_id = models.IntegerField(db_index=True)
    path = models.CharField(max_length=50)
    
#作者資料
class Author(models.Model):
    author_id = models.IntegerField(primary_key=True, db_index=True)
    authorName = models.CharField(max_length=50)
    
    def __str__(self):
        return self.authorName

#出版社資料
class Publisher(models.Model):
    publisher_id = models.IntegerField(primary_key=True, db_index=True)
    publisherName = models.CharField(max_length=50)

    def __str__(self):
        return self.publisherName

#書籍評論
class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    product_id = models.IntegerField(db_index=True)
    member_id = models.IntegerField(db_index=True)
    evaluate = models.CharField(max_length=1000)

#購物車內容
class Order_product(models.Model):
    orderProduct_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(db_index=True)
    product_id = models.IntegerField(db_index=True)
    orderProductQuantity = models.IntegerField(default=0)

#訂購資料
class Order_data(models.Model):
    order_id = models.AutoField(primary_key=True)
    member_id = models.IntegerField(db_index=True)
    orderTime = models.DateTimeField()
    orderDiscount = models.IntegerField(default=0)
    orderDeliverFee = models.IntegerField(default=0)
    orderAmount = models.IntegerField(default=0)
    orderPayment = models.CharField(max_length=10)
    orderName = models.CharField(max_length=50)
    orderPhone = models.CharField(max_length=10)
    orderAddress = models.CharField(max_length=50)