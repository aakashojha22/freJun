# freJun
gitURL :- https://github.com/aakashojha22/freJun
HostedURL :- https://fre-jun.herokuapp.com/
1. Install all the dependency from <i>requirements.txt</i> .
2. Install Postgresql.
3. Fetch postgres data dump from **schema.sql**

<p><i>Above data contains two tables:
a) account (id, auth_id, username)
b) phone_number (id, number, account_id (FK to account) )</i></p>

4. Make sure migrate database before running server.

5. Project contain to endpoint i.e.
<i>

API /inbound/sms/
Input parameters
parameter required example

from (string min length 6 max length 16) Ex :- 91983435345

to (string min length 6 max length 16) Ex :- 14152243533

text (string min length 1 max length 120) Ex :- STOP, Hello World, ...

API /outbound/sms/
Input parameters
parameter required example

from (string min length 6 max length 16) Ex :- 919823243432

to (string min length 6 max length 16) Ex :- 919343542749

text (string min length 1 max length 120) Ex :- 'faegtef'

</i>