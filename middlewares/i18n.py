from aiogram.utils.i18n import I18n, I18nMiddleware

i18n = I18n(
    path="locales",         # Путь к папке с переводами
    default_locale="en",    # Язык по умолчанию
    domain="messages",      # Имя .po/.mo файлов
)

# Создаём мидлварь
i18n_middleware = I18nMiddleware(i18n)
