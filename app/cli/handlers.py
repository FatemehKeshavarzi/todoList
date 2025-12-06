from datetime import date
from typing import Literal
import logging
from app.services.project_service import ProjectService
from app.services.task_service import TaskService
from app.repositories.project_repository import InMemoryProjectRepository, SQLProjectRepository
from app.repositories.task_repository import InMemoryTaskRepository, SQLTaskRepository
from app.utils import func
from app.models import TaskStatus, Project, Task
from config import STORAGE

logger = logging.getLogger(__file__)

class CLIHandler:
    task_service = TaskService(task_repo=InMemoryTaskRepository())

    def __init__(self, storage:Literal['memory', 'sql'] = STORAGE) -> None:

        """
        NOTE: The CLI interface is deprecated. Please start using the API endpoint instead.
        """
        logger.warning('Warning: The CLI interface is deprecated. Please start using the API endpoint instead.')


        if storage == 'memory':
            self.project_service = ProjectService(project_repo=InMemoryProjectRepository(), task_repo=InMemoryTaskRepository())
            self.task_service = TaskService(task_repo=InMemoryTaskRepository())
        elif storage == 'sql':
            self.project_service = ProjectService(project_repo=SQLProjectRepository(), task_repo=SQLTaskRepository())
            self.task_service = TaskService(task_repo=SQLTaskRepository())
        else:
            raise NotImplementedError('invalid storage type')

        print('>>>>>>>>> CLI <<<<<<<<<')
        self.start()
        

    def start(self):
        print('=============MENU=============')
        print('Enter option:')
        print('1 - Show projects')
        print('2 - Add project')
        print('3 - Update project')
        print('4 - Delete project')
        print('5 - Show project tasks')
        print('6 - Add task')
        print('7 - Update task')
        print('8 - Delete task')
        print('10 - Exit')
        print('==============================')
        option = input('Option => ')
        if option == '1':
            self._list_projects()
        elif option == '2':
            self._create_project()
        elif option == '3':
            self._update_project()
        elif option == '4':
            self._delete_project()
        elif option == '5':
            self._list_project_tasks()
        elif option == '6':
            self._create_task()
        elif option == '7':
            self._update_task()
        elif option == '8':
            self._delete_task()
        elif option == '10':
            return
        else:
            print('Invalid option')
            self.start()
    
    def _list_projects(self):
        print('> Projects:')
        projects = self.project_service.list_projects()
        if projects:
            for project in projects:
                self._print_project(project=project)
        else:
            print('There isn\'t any project')
        self.start()

    def _update_project(self):
        print('> Update project:')
        project_code = int(input('project_code => '))
        title = input('title => ')
        description = input('description => ')
        self.project_service.update_project(project_code=project_code, title=title, description=description)
        print('Updated successfully')
        self.start()

    def _delete_project(self):
        print('> Delete project:')
        project_code = int(input('project_code => '))
        self.project_service.delete_project(project_code=project_code)
        print('Deleted successfully')
        self.start()

    def _list_project_tasks(self):
        print('> Project tasks:')
        project_code = int(input('project_code => '))
        tasks = self.project_service.list_project_tasks(project_code=project_code)
        if tasks:
            for task in tasks:
                self._print_task(task=task)
        else:
            print('There isn\'t any task')
        self.start()
    
    def _create_project(self):
        print('> Add project:')
        title = input('title => ')
        description = input('description => ')
        project = self.project_service.create_project(title=title, description=description)
        print('> New project')
        self._print_project(project=project)
        self.start()

    def _create_task(self):
        print('> Add task:')
        project_code = int(input('project_code => '))
        title = input('title => ')
        description = input('description => ')
        input_deadline = input('deadline date (optional) eg:2000-10-30 => ')
        deadline : date | None = func.parse_deadline(deadline=input_deadline) if input_deadline else None
        status : str = input('status [done, doing, todo] (default=todo)  => ') or 'todo'
        task = self.task_service.create_task(project_code=project_code,
                                             title=title,
                                             description=description,
                                             deadline=deadline,
                                             status=TaskStatus(status))
        print('> New task')
        self._print_task(task=task)
        self.start()

    def _update_task(self):
        print('> Update task:')
        task_code = int(input('task_code => '))
        title = input('title => ')
        description = input('description => ')
        input_deadline = input('deadline date (optional) eg:2000/10/30 => ')
        deadline : date | None = func.parse_deadline(deadline=input_deadline) if input_deadline else None
        status : str = input('status [done, doing, todo] (default=todo)  => ') or 'todo'
        task = self.task_service.update_task(task_code=task_code,
                                      title=title,
                                      description=description,
                                      deadline=deadline,
                                      status=TaskStatus(status))
        print('Updated successfully')
        self.start()

    def _delete_task(self):
        print('> Delete task:')
        task_code = int(input('task_code => '))
        self.task_service.delete_task(task_code=task_code)
        print('Deleted successfully')
        self.start()


    def _print_project(self, project:Project):
        print('---------')
        print(f'code: {project.code}')
        print(f'title: {project.title}')
        print(f'description: {project.description}')
        print(f'created_time: {project.created_time}')

    def _print_task(self, task:Task):
        print('---------')
        print(f'task_code: {task.code}')
        print(f'title: {task.title}')
        print(f'description: {task.description}')
        print(f'status: {task.status}')
        print(f'created_time: {task.created_time}')
        print(f'deadline: {task.deadline}')
        print(f'closed_at: {task.closed_at}')

        