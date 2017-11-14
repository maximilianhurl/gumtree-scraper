from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.latest_only_operator import LatestOnlyOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from pathlib import Path
from project.emails import send_email
from project.reports import generate_report

CODE_DIR = Path(__file__).parent.parent

default_args = {
    'owner': 'MAX',
    'depends_on_past': False,
    'start_date': datetime(2015, 6, 1),
    'email': ['max@maxhurl.co.uk'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
    'catchup': False
}

dag = DAG(
    'gumtree_scraper',
    default_args=default_args,
    schedule_interval=timedelta(minutes=5),
    catchup=False
)

op_parent = LatestOnlyOperator(
    task_id='latest_only',
    dag=dag
)

op_scrape = BashOperator(
    task_id='scrape_gumtree',
    bash_command=f'cd {CODE_DIR} && env/bin/scrapy runspider project/spider.py',
    # TODO: Improve failure callback
    on_failure_callback=lambda c: send_email('Gumtree scraper failed', 'oh no!'),
    dag=dag
)

op_report = PythonOperator(
    python_callable=generate_report,
    task_id='generate_report',
    retries=0,
    dag=dag
)

op_parent >> op_scrape >> op_report
