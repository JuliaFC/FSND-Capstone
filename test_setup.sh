#!/bin/sh -x

# create database with name as capstone_fsnd_test
DATABASE_NAME='capstone_fsnd_test'
if psql -lqt | cut -d \| -f 1 | grep -qw $DATABASE_NAME; then
    echo "A database with the name $DBNAME already exists."
    echo "Drop $DATABASE_NAME and create a new one."
    dropdb $DATABASE_NAME
fi
createdb $DATABASE_NAME

# Export the environment variables and set up for the server
export DATABASE_URL='postgresql://localhost:5432/capstone_fsnd_test' 
export SUPREME_LEADER='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJyQmlLREd2NEJScWNxdkZMY2tnLSJ9.eyJpc3MiOiJodHRwczovL2Nvd2ZmZWVzaG9wLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1Zjk4MGMyODczMDVhMjAwNzY5MGZiODMiLCJhdWQiOiJjYXBzdG9uZS1hcGkiLCJpYXQiOjE2MDM4MDA2MDYsImV4cCI6MTYwMzg4NzAwNiwiYXpwIjoiOXRoT2JEWWlseGt4alk4Y1d2eW5UaUY0aGpINXZ5eEQiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpiYXNlIiwiZGVsZXRlOmNyZXciLCJnZXQ6YmFzZSIsImdldDpjcmV3IiwicGF0Y2g6YmFzZSIsInBhdGNoOmNyZXciLCJwb3N0OmJhc2UiLCJwb3N0OmNyZXciXX0.YbT7p-BIRFeMfCNkRD5NXz9WN9gAs3wpxmLzKbQhoDf3P7PKRmIQnMDN1XdbwahavbG2R4-40QJWxn9aRVlR5AE4iOmea69kJ21zyNa6aq_yrbKEXO5AufCxvumSsGtjQEJAPYRy5xcTGh6H26CD4aejh3mSGThx1VSnxXuE8tuxAujo2RP5ze7gRPT5awYZ5LaL8Cn6DYKD0KVye532chkswSBEuAoaaWpQwaV3jFblgIHsPwhzrdXMQ5eUOE6xKSlFZFG-0ciFSkUKrjjN0Cf2JHvj6j98s-tQLjdb2XYaDJsN8T4ggz1j6I73krPRiIaroUWqZHfSrXyTs3zm4Ate'
export CREW_TOKEN='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJyQmlLREd2NEJScWNxdkZMY2tnLSJ9.eyJpc3MiOiJodHRwczovL2Nvd2ZmZWVzaG9wLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1Zjk4MTMwMmVkYzY0YTAwNjgyMDAyNGUiLCJhdWQiOiJjYXBzdG9uZS1hcGkiLCJpYXQiOjE2MDM4Mzg4OTMsImV4cCI6MTYwMzkyNTI5MywiYXpwIjoiOXRoT2JEWWlseGt4alk4Y1d2eW5UaUY0aGpINXZ5eEQiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDpiYXNlIiwiZ2V0OmNyZXciXX0.lJXm7H8XUhgFmnGV6IKviuQCsKPPiJXaDP_U1PEkpRzsd1QEIupe9NucvIm_NEQp274zBpfkKOgwmN3E9K2NIHvxC5JDaWEek-jCU4Sr8aJYFVWR9QNpXfiqiHCeI635DDvEoiNWMO1TdIuPzrAcRVjDUiqdqiTqXLhuUhO4uS-qC2JVB3BKmC5gLLOqJV6ONr9NH-zS0AncNF2ElrShJoP3tHEu_AvTA1yCg9AthdYb0kqbW02lZ7ULYqOq-1pN2ouILfYdQ44qDHxlAoyRuEvzzpPu51uTTcYgL6BlAoGWNRMQ0fSm4Qph2TtieHWH2nhd4egmkcOroAaZkLUxnQ' 
python3 -m test.py -v