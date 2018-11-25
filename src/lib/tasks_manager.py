class Task_manager():

    def __init__(self, bdd):

        self.bdd = bdd
        self.max_running_tasks_number = 20
        self.max_days_old_db_entries = 180
        self.tasks_instances_dict = []
        self.utilities_timer = 10

    def create_task(self, command):
        pass

    def read_tasks(self):
        pass

    def read_task(self, task_id):
        pass

    def update_task(self, task_id, element_to_add):
        pass

    def delete_task(self, task_id):
        pass

    def update_taks_status_from_os(self, task_id, status):
        pass

    def kill_task(task_id):
        pass

    def get_running_tasks(self):
        pass

    def vacuum_tasks(self):
        pass

    def set_max_day_old_db_entries(self, value):
        self.max_days_old_db_entries = value

    def set_max_running_task_number(self, value):
        self.max_running_tasks_number = value
