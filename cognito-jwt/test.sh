#!/bin/bash

if [ "$USER_EMAIL" = "" ]; then
  echo Please specify '$USER_EMAIL' in the environment
  exit 1
fi

## Create pool and client

pool_id=$(awslocal cognito-idp create-user-pool --pool-name test | jq -rc ".UserPool.Id")
client_id=$(awslocal cognito-idp create-user-pool-client --user-pool-id $pool_id --client-name test-client | jq -rc ".UserPoolClient.ClientId")
echo "Working with user pool ID $pool_id, user pool client ID $client_id"

## User sign up

PASSWORD=12345678Aw!
echo "Starting user signup flow"
awslocal cognito-idp sign-up --client-id $client_id --username example_user --password $PASSWORD --user-attributes Name=email,Value="$USER_EMAIL"
echo "Please check email inbox for $USER_EMAIL, and enter the confirmation code below:"
read code
awslocal cognito-idp confirm-sign-up --client-id $client_id --username example_user --confirmation-code $code
# Alternative to the above line
# awslocal cognito-idp admin-confirm-sign-up --user-pool-id $pool_id --username example_user

# Update user attributes

echo "Updating user attributes"
awslocal cognito-idp admin-update-user-attributes --user-pool-id $pool_id --username example_user --user-attributes Name=preferred_username,Value=nickname

# Start auth flow

echo "Starting auth flow"
awslocal cognito-idp initiate-auth --client-id $client_id --auth-flow USER_PASSWORD_AUTH --auth-parameters USERNAME=example_user,PASSWORD=$PASSWORD

# Restore forgotten password

echo "Restore forgotten password"
awslocal cognito-idp forgot-password --client-id $client_id --username example_user
echo "Please check email inbox for $USER_EMAIL, and enter the password reset code below:"
read code
NEW_PASSWORD=new_password123A!
echo "Setting new password with the given verification code"
awslocal cognito-idp confirm-forgot-password --client-id $client_id --username example_user --confirmation-code $code --password $NEW_PASSWORD
echo "Attempting to authenticate with the new password"
awslocal cognito-idp initiate-auth --client-id $client_id --auth-flow USER_PASSWORD_AUTH --auth-parameters USERNAME=example_user,PASSWORD=$NEW_PASSWORD

## "Admin creates the user" with "admin initiates auth" workflow

echo "Create new user as admin"
awslocal cognito-idp admin-create-user --user-pool-id $pool_id --username example_user2
echo "Attempting to authenticate the not yet verified user - this request should FAIL"

awslocal cognito-idp admin-initiate-auth --user-pool-id $pool_id --client-id $client_id --auth-flow ADMIN_USER_PASSWORD_AUTH --auth-parameters USERNAME=example_user2,PASSWORD=$PASSWORD
echo $?
echo "Setting password of new user"
awslocal cognito-idp admin-set-user-password --user-pool-id $pool_id --username example_user2 --password $PASSWORD --permanent
echo "Attempting to authenticate the new user"
awslocal cognito-idp admin-initiate-auth --user-pool-id $pool_id --client-id $client_id --auth-flow ADMIN_USER_PASSWORD_AUTH --auth-parameters USERNAME=example_user2,PASSWORD=$PASSWORD

## "Admin creates the user" with "user initiates auth" workflow

awslocal cognito-idp admin-create-user --user-pool-id "$pool_id" --username example_user3 --temporary-password "ChangeMe"

session=$(awslocal cognito-idp initiate-auth --auth-flow "USER_PASSWORD_AUTH" --auth-parameters USERNAME=example_user3,PASSWORD="ChangeMe" --client-id "$client_id" | jq -r '.Session')

awslocal cognito-idp admin-respond-to-auth-challenge --user-pool-id "$pool_id" --client-id "$client_id" --challenge-responses "NEW_PASSWORD=FinalPassword,USERNAME=example_user3" --challenge-name NEW_PASSWORD_REQUIRED --session "$session"
