mkdir -p ~/.streamlit/
echo "\
[general]\n\
email = \"almmello@gmail.com\"\n\
" > ~/.streamlit/credentials.toml
echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
echo $GOOGLE_CREDENTIALS | base64 --decode > google-credentials.json