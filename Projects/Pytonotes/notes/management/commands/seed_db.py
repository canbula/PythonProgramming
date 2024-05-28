from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from notes.models import Workspace, Page

class Command(BaseCommand):
    help = 'Seed the database with sample data'

    def handle(self, *args, **kwargs):
        User = get_user_model()

        # Clear existing data
        User.objects.all().delete()
        Workspace.objects.all().delete()
        Page.objects.all().delete()

        # Create sample users
        users = [
            User.objects.create_user(email='user1@example.com', name='User One', password='password1'),
            User.objects.create_user(email='user2@example.com', name='User Two', password='password2'),
            User.objects.create_user(email='user3@example.com', name='User Three', password='password3'),
            User.objects.create_user(email='user4@example.com', name='User Four', password='password4'),
        ]

        # Create sample workspaces and pages with simple text content
        for user in users:
            for i in range(3):
                workspace = Workspace.objects.create(user=user, name=f"{user.name.split()[0]}'s Workspace {i+1}", icon='fa-solid fa-w')
                workspace.members.add(user)
                for j in range(5):
                    Page.objects.create(
                        workspace=workspace,
                        title=f"{workspace.name} Page {j+1}",
                        icon='fa-solid fa-file',
                        content=f"This is the content of {workspace.name} Page {j+1}."
                    )

        # Create shared workspaces
        shared_workspace = Workspace.objects.create(user=users[0], name="Shared Workspace 1", icon='fa-solid fa-w')
        shared_workspace.members.set(users)
        for i in range(5):
            Page.objects.create(
                workspace=shared_workspace,
                title=f"{shared_workspace.name} Page {i+1}",
                icon='fa-solid fa-file',
                content=f"This is the content of {shared_workspace.name} Page {i+1}."
            )

        self.stdout.write(self.style.SUCCESS('Database seeded successfully'))