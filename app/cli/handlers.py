from pprint import pprint
from typing import Literal
from app.services.project_service import ProjectService
from app.services.task_service import TaskService
from app.repositories.project_repository import in_memory_project_repo
from app.repositories.task_repository import in_memory_task_repo


class CLIHandler:
    project_service = ProjectService(project_repo=in_memory_project_repo, task_repo=in_memory_task_repo)
    task_service = TaskService(task_repo=in_memory_task_repo)

    def __init__(self) -> None:
        print('>>>>>>>>> CLI <<<<<<<<<')
        self.start()

    def start(self):
        print('\n\nEnter option:')
        print('1 - Show projects')
        print('2 - Add project')
        print('3 - Update project')
        print('4 - Delete project')
        print('5 - Show project tasks')
        print('6 - Add task')
        print('7 - Update task')
        print('8 - Delete task')
        print('10 - Exit\n')
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
                pprint(project)
        else:
            print('There isn\'t any project')
        self.start()

    def _update_project(self):
        print('> Update project:')
        project_id = int(input('project_id => '))
        title = input('title => ')
        description = input('description => ')
        self.project_service.update_project(project_id=project_id, title=title, description=description)
        print('Updated successfully')
        self.start()

    def _delete_project(self):
        print('> Delete project:')
        project_id = int(input('project_id => '))
        self.project_service.delete_project(project_id=project_id)
        print('Deleted successfully')
        self.start()

    def _list_project_tasks(self):
        print('> Project tasks:')
        project_id = int(input('project_id => '))
        tasks = self.project_service.list_project_tasks(project_id=project_id)
        for task in tasks:
            pprint(task)
        self.start()
    
    def _create_project(self):
        print('> Add project:')
        title = input('title => ')
        description = input('description => ')
        project = self.project_service.create_project(title=title, description=description)
        print('> New project')
        pprint(project)
        self.start()

    def _create_task(self):
        print('> Add task:')
        project_id = int(input('project_id => '))
        title = input('title => ')
        description = input('description => ')
        deadline = input('deadline date (optional) eg:2000/10/30 => ')
        deadline = None if not deadline else deadline
        status : str = input('status [done, doing, todo] (default=todo)  => ') or 'todo'
        task = self.task_service.create_task(project_id=project_id,
                                             title=title,
                                             description=description,
                                             deadline=deadline,
                                             status=status)
        print('> New task')
        pprint(task)
        self.start()

    def _update_task(self):
        print('> Update task:')
        task_id = int(input('task_id => '))
        title = input('title => ')
        description = input('description => ')
        deadline = input('deadline date (optional) eg:2000/10/30 => ')
        status : str = input('status [done, doing, todo] (default=todo)  => ') or 'todo'
        task = self.task_service.update_task(task_id=task_id,
                                      title=title,
                                      description=description,
                                      deadline=deadline,
                                      status=status)
        print('Updated successfully')
        self.start()

    def _delete_task(self):
        print('> Delete task:')
        task_id = int(input('task_id => '))
        self.task_service.delete_task(task_id=task_id)
        print('Deleted successfully')
        self.start()


        
        