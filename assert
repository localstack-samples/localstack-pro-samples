# A small helper to throw an error if the parameters do no match. Requires 'set -e' in the calling script to cause a full program abortion on error.
if ! [ "'$1'" $2 "'$3'" ]; then
  echo assert "\"$1 $2 $3\"" did not hold, exiting...
  exit 1
fi
