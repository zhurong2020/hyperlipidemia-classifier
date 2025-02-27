   #!/bin/bash

   # Enter project directory
   cd ~/hyperlipidemia_web

   # Recreate virtual environment if needed
   if [ ! -d "venv" ]; then
       python3 -m venv venv
   fi

   # Activate virtual environment
   source venv/bin/activate

   # Pull latest code
   git pull origin main

   # Install dependencies
   pip install -r requirements.txt

   # Restart Flask application
   pkill -f run.py
   nohup python3 run.py &