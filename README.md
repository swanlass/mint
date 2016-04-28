# mint
Description: Analyze your Mint data in Looker! The get_transactions.py is a python script which authenticates the user into Mint, downloads transaction data, and loads it into a MySQL database. 

<b>Steps:</b>
1. Create your Mint account.
2. Set up your Looker server: http://www.looker.com/docs/setup-and-management/on-prem-install
3. Set up your database.
4. Clone this repo to your machine.
5. Modify the get_transactions python script with your variables. The variables are found on lines 11 through 17.
6. Execute the load_mint shell script by typing ./load_mint in the terminal. Of course you can schedule this as a cron job.

<b>Notes:</b>
- If you would like to do more complex stuff then what my script offers, consider using this api: https://github.com/mrooney/mintapi
- If you would like to use a postgres db instead, it should be pretty easy to get_transactions.py for a postgres library instead of the MySQLdb library. I think importing and using the psycopg2 library would work.







