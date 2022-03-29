from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(unique=True, max_length=16, null=True, blank=True, verbose_name='Номер телефона')
    birth_date = models.DateField(null=True, blank=True, verbose_name='День рождения')


User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Bb(models.Model):
    title = models.CharField(max_length=50, verbose_name='Товар',
                             validators=[validators.MinLengthValidator(3,
                                                                       message='Название должно быть от 3 символов')])
    content = models.TextField(null=True, blank=True, verbose_name='Описание',
                               validators=[validators.MinLengthValidator(5,
                                                                         message='Описание должно быть от 5 символов')])
    price = models.FloatField(null=True, blank=True, verbose_name='Цена')
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')
    rubric = models.ForeignKey('Rubric', null=True, on_delete=models.PROTECT,
                               verbose_name='Рубрика')
    buser = models.CharField(max_length=20, null=True, blank=True, verbose_name='Пользователь')

    class Meta:
        verbose_name_plural = 'Объявления'
        verbose_name = 'Объявление'
        ordering = ['-published']

    class Kinds(models.TextChoices):
        BUY = 'b', 'Куплю'
        SELL = 's', 'Продам'
        EXCHANGE = 'c', 'Обменяю'
        RENT = 'r', 'Сдам в аренду'

    kind = models.CharField(max_length=1, choices=Kinds.choices, default=Kinds.SELL, verbose_name='Тип')

    def clean(self):
        errors = {}
        if not self.content:
            errors['content'] = ValidationError('Заполните описание')
        if self.price and self.price < 0:
            errors['price'] = ValidationError('Цена не может быть отрицательной!')
        if errors:
            raise ValidationError(errors)

    def user_dir(instance, filename):
        return '{0}/images/{1}'.format(instance.buser, filename)

    photo = models.ImageField(upload_to=user_dir, null=True, blank=True, verbose_name='Фото')


class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Рубрики'
        verbose_name = 'Рубрика'
        ordering = ['name']


class AdvUser(models.Model):
    is_activated = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class CarBrands(models.Model):
    class CarBrand(models.TextChoices):
        AUDI = 'Audi', 'Audi'
        BMW = 'BMW', 'BMW'
        CHERY = 'Chery', 'Chery'
        CHEVROLET = 'Chevrolet', 'Chevrolet'
        CITROEN = 'Citroen', 'Citroen'
        DAEWOO = 'Daewoo', 'Daewoo'
        FORD = 'Ford', 'Ford'
        GAZ = 'Газ', 'Газ'
        GEELY = 'Geely', 'Geely'
        HAVAL = 'Haval', 'Haval'
        HONDA = 'Honda', 'Honda'
        HYUNDAI = 'Hyundai', 'Hyundai'
        INFINITI = 'Infiniti', 'Infiniti'
        KIA = 'KIA', 'KIA'
        LADA = 'Lada', 'Lada'
        LANDROVER = 'Land Rover', 'Land Rover'
        LEXUS = 'Lexus', 'Lexus'
        MINI = 'Mini', 'Mini'
        MAZDA = 'Mazda', 'Mazda'
        MERCEDES = 'Mercedes-Benz', 'Mercedes-Benz'
        NISSAN = 'Nissan', 'Nissan'
        OPEL = 'Opel', 'Opel'
        PORSCHE = 'Porsche', 'Porsche'
        RENAULT = 'Renault', 'Renault'
        SKODA = 'Skoda', 'Skoda'
        SUZUKI = 'Suzuki', 'Suzuki'
        TOYOTA = 'Toyota', 'Toyota'
        VOLKSWAGEN = 'Volkswagen', 'Volkswagen'
        VOLVO = 'Volvo', 'Volvo'
        __empty__ = 'Выберите марку машины'

    name = models.CharField(max_length=20, db_index=True, choices=CarBrand.choices, verbose_name='Марка')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Марки авто'
        verbose_name = 'Марка авто'
        ordering = ['name']


class CarModels(models.Model):
    name = models.CharField(max_length=20, null=True, verbose_name='Модель')
    brand = models.ForeignKey('CarBrands', db_index=True, null=True, on_delete=models.CASCADE, verbose_name='Марка')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Модели авто'
        verbose_name = 'Модель авто'
        ordering = ['name']


class Car(Bb):
    mileage = models.IntegerField(null=True, blank=True, verbose_name='Пробег')
    year = models.IntegerField(null=False, default='2020', verbose_name='Год выпуска')
    model = models.ForeignKey('CarModels', null=True, on_delete=models.PROTECT, verbose_name='Модель')
    is_competitive = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Авто объявления'
        verbose_name = 'Авто объявление'
        ordering = ['-published']

    class CarBody(models.IntegerChoices):
        SEDAN = 1, 'Седан'
        COUPE = 2, 'Купе'
        HATCHBACK3 = 3, 'Хэтчбек 3 дв.'
        HATCHBACK5 = 4, 'Хэтчбек 5 дв.'
        OFFROAD3 = 5, 'Внедорожник 3 дв.'
        OFFROAD5 = 6, 'Внедорожник 5 дв.'
        LIFTBACK = 7, 'Лифтбек'
        CABRIOLET = 8, 'Кабриолет'
        UNIVERSAL = 9, 'Универсал'
        LIMO = 10, 'Лимузин'

    body = models.PositiveSmallIntegerField(choices=CarBody.choices, default=CarBody.SEDAN, verbose_name='Тип кузова')

    class EngineType(models.TextChoices):
        BENZIN = 'b', 'Бензин'
        DIESEL = 'd', 'Дизель'
        ELECTRO = 'e', 'Электро'
        HIBRID = 'h', 'Гибрид'
        GAS = 'g', 'Газ'

    engine_type = models.CharField(max_length=1, choices=EngineType.choices, default=EngineType.BENZIN,
                                   verbose_name='Тип двигателя')

    class GearShift(models.TextChoices):
        ROBOT = 'r', 'Роботизированная'
        CLASSICAUTO = 'a', 'Автоматическая'
        VARIATOR = 'v', 'Вариатор'
        MANUAL = 'm', 'Механическая'

    gear = models.CharField(max_length=1, choices=GearShift.choices, default=GearShift.MANUAL,
                            verbose_name='Коробка передач')

    class WheelDrive(models.IntegerChoices):
        FRONT = 1, 'Передний'
        REAR = 2, 'Задний'
        FULL = 3, 'Полный'

    drive = models.PositiveSmallIntegerField(choices=WheelDrive.choices, default=WheelDrive.FRONT,
                                             verbose_name='Тип привода')

    class CarStatus(models.TextChoices):
        NEW = 'n', 'Новая'
        USED = 'u', 'С пробегом'

    status = models.CharField(max_length=1, choices=CarStatus.choices, default=CarStatus.USED, verbose_name='Состояние')

    class CarEquipment(models.TextChoices):
        HIGH = 'h', 'Максимальная'
        MIDDLE = 'm', 'Средняя'
        START = 's', 'Базовая'

    equip = models.CharField(max_length=1, choices=CarEquipment.choices, default=CarEquipment.START,
                             verbose_name='Комплектация')

    class CarColor(models.IntegerChoices):
        RED = 1, 'Красный'
        GREEN = 2, 'Зеленый'
        BLUE = 3, 'Синий'
        WHITE = 4, 'Белый'
        BLACK = 5, 'Черный'
        YELLOW = 6, 'Желтый'
        LIGTH_BLUE = 7, 'Голубой'
        ORANGE = 8, 'Оранжевый'
        PINK = 9, 'Розовый'
        BROWN = 10, 'Коричневый'
        GREY = 11, 'Серый'
        VINOUS = 12, 'Бордовый'
        BEIGE = 13, 'Бежевый'
        GOLDEN = 14, 'Золотой'

    color = models.PositiveSmallIntegerField(choices=CarColor.choices, default=CarColor.WHITE, verbose_name='Цвет')

    class CarPts(models.IntegerChoices):
        ORIGINAL = 1, 'Оригинал'
        DUBLICATE = 2, 'Дубликат'

    pts = models.PositiveSmallIntegerField(choices=CarPts.choices, default=CarPts.ORIGINAL, verbose_name='ПТС')

    class CarOwners(models.IntegerChoices):
        ONE = 1, 'Один'
        TWO = 2, 'Два'
        MORE = 3, 'Три и более'
        NEW = 4, 'Новый авто'

    owners = models.PositiveSmallIntegerField(choices=CarOwners.choices, default=CarOwners.ONE,
                                              verbose_name='Собственников в ПТС')


class Message(models.Model):
    content = models.TextField()
    name = models.CharField(max_length=20)
    email = models.EmailField()

    class Meta:
        abstract = True


class PrivateMessage(Message):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    email = None
