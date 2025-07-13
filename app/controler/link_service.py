from controler.IService import IService
from logger import log
from model.schemas.link_schema import ClassSession, Subject


class LinkService(IService):
    def __init__(self, link):
        super().__init__()
        self.link = link

    def save(self, e):
        key = e.control.data
        value = e.control.value

        self.data[key] = value
        log.debug("дані %r збережено у словнику", key)


    def get(self, subject_name):
        return self.link[subject_name]


    def save_to_file(self, switch_content, e=None):
        pair_name = self.data.get("pair_name", "")

        if not pair_name:
            # TODO: повідомлення користувачу
            log.warning("збереження посилань без назви пари неможливе")
            return

        log.info("спроба зберегти посилання у файл...")

        self.link.subjects[pair_name] = Subject(
            lecture=ClassSession(zoom=self.data.get("lecture_zoom", ""), attendance=self.data.get("lecture_attendance", "")),
            practice=ClassSession(zoom=self.data.get("practice_zoom", ""), attendance=self.data.get("practice_attendance", "")),
            laboratory=ClassSession(zoom=self.data.get("laboratory_zoom", ""), attendance=self.data.get("laboratory_attendance", "")),
        )
        log.debug("створено об'єкт для збереження у файл")

        self.data = {}
        log.debug("попередні дані були очищені")

        self.link.save()
        log.info("посилання було успішно збережено у файлі")
        switch_content(e)

    def get_subjects_name(self):
        return self.link.subjects.keys()

    def get_data_about_subject(self, subject):
        return self.link.subjects[subject]

    def delete(self, e, switch_content):
        subject_name = e.control.data.get("lesson_name", "")
        if not subject_name:
            # TODO: повідомлення для користувача
            log.warning("не надано назву пари для видалення")
            return

        self.link.subjects.pop(subject_name)

        log.info('посилання для %r було видалено з файлу', subject_name)
        self.link.save()
        log.debug('дані оновлені у файлі')

        if not switch_content:
            # TODO: повідомлення для користувача
            log.warning("неможливо оновити картки у представлені")
            return

        switch_content(e)


