FROM public.ecr.aws/lambda/python:3.7

# Copy function code
COPY app.py ${LAMBDA_TASK_ROOT}
COPY rds_config.py ${LAMBDA_TASK_ROOT}
COPY rds_connect.py ${LAMBDA_TASK_ROOT}
# Install the function's dependencies using file requirements.txt
# from your project folder.

#Set Environ value for RDS
ENV RDS_ENDPOINT ai-rds.cdfnd5ogvaqo.ap-northeast-2.rds.amazonaws.com
ENV USERNAME brokurly
ENV PASSWORD Kosa0401!
ENV DB_NAME item_ingredients
ENV TABLE_NAME Item

COPY requirements.txt  .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"
# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app.handler" ]
