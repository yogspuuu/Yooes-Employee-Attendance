import os
import subprocess

def run(current_path):
    # Clear all cache
    os.system(f'cd {current_path} && php artisan view:clear')
    os.system(f'cd {current_path} && php artisan route:cache')
    os.system(f'cd {current_path} && php artisan config:cache')

    # Run laravel and flask (For development only!)
    subprocess.run(f'cd {current_path} && php artisan serve & cd {current_path}/engine && python3 run_flask.py', shell=True)

if __name__ == '__main__':
    run(os.getcwd())
    