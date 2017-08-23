import os

from django.core.management import call_command

try:
    import uwsgi
    from uwsgidecorators import timer, cron

    print("We have a uWSGI")
    has_uwsgi = True
except ImportError:
    print("We have no uWSGI")
    has_uwsgi = False


def single_instance_command(command_name):
    """Runs command only on one instance of a uWSGI legion"""

    if os.getenv("CFG_I_AM_CRON"):
        print("I am the lord.")
        print("Running %s" % command_name)
        call_command(command_name, interactive=False)

if has_uwsgi:
    @cron(0, 1, -1, -1, -1)
    def clearsessions(signum):
        single_instance_command('clearsessions')

    @cron(0, 0, -1, -1, -1, target='mule')
    def update_index(signum):
        single_instance_command('update_index')

    def import_research_summaries(signum):
        """
        Currently the API has limited availability,
        it is open only during on these days and time:
        Monday, Wednesday, Thursday – between 6:00 - 8:00 am UTC

        Note that server is London time, so we have to run this cron
        between 7am and 9am.
        """
        single_instance_command('import_research_summaries')

    # Monday at 7:30am London time (6:30am UTC)
    cron(30, 7, -1, -1, 1, target='mule')(import_research_summaries)
    # Wednesday at 7:30am London time (6:30am UTC)
    cron(30, 7, -1, -1, 3, target='mule')(import_research_summaries)
    # Thursday at 7:30am London time (6:30am UTC)
    cron(30, 7, -1, -1, 4, target='mule')(import_research_summaries)

    @timer(300)
    def publish_scheduled_pages(cron):
        single_instance_command('publish_scheduled_pages')
