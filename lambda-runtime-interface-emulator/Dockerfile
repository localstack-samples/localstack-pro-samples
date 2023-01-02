FROM amazonlinux:latest

# Define custom function directory
ARG FUNCTION_DIR="/function"

# Install ruby
RUN amazon-linux-extras install -y ruby2.6

# Install bundler
RUN gem install bundler

# Install the Runtime Interface Client
RUN gem install aws_lambda_ric

# Copy function code
RUN mkdir -p ${FUNCTION_DIR}
RUN mkdir -p /var/rapid
COPY app.rb ${FUNCTION_DIR}

WORKDIR ${FUNCTION_DIR}

ENTRYPOINT ["/usr/local/bin/aws_lambda_ric"]
CMD ["app.App::Handler.process"]
