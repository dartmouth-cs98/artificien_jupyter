#Base image
FROM jupyterhub/jupyterhub:latest

#USER root

# update Ubuntu
RUN apt-get update


# Install jupyter, awscli and s3contents (for storing notebooks on S3)
RUN pip install jupyter  && \
    pip install s3contents  && \
    pip install awscli --upgrade --user  && \
    mkdir /etc/jupyter
 
#S3ContentManager Config
RUN echo 'from s3contents import S3ContentsManager' >> /etc/jupyter/jupyter_notebook_config.py  && \
    echo 'c = get_config()' >> /etc/jupyter/jupyter_notebook_config.py  && \
    echo 'c.NotebookApp.contents_manager_class = S3ContentsManager' >> /etc/jupyter/jupyter_notebook_config.py  && \
    echo 'c.S3ContentsManager.access_key_id = "xxxxxxxx"' >> /etc/jupyter/jupyter_notebook_config.py  && \
    echo 'c.S3ContentsManager.secret_access_key = "xxxxxxxx"' >> /etc/jupyter/jupyter_notebook_config.py  && \
    echo 'c.S3ContentsManager.bucket = "vishaljuypterhub"' >> /etc/jupyter/jupyter_notebook_config.py

#JupyterHub Config
RUN echo "c = get_config()" >> /srv/jupyterhub/jupyterhub_config.py  && \
    echo "c.Spawner.env_keep = ['AWS_DEFAULT_REGION','AWS_EXECUTION_ENV','AWS_REGION','AWS_CONTAINER_CREDENTIALS_RELATIVE_URI','ECS_CONTAINER_METADATA_URI']" >> /srv/jupyterhub/jupyterhub_config.py  && \
    echo "c.Spawner.cmd = ['/opt/conda/bin/jupyterhub-singleuser']" >> /srv/jupyterhub/jupyterhub_config.py

#Add PAM users
RUN useradd --create-home user3  && \
    echo "user3:user3"|chpasswd  && \
    echo "export PATH=/opt/conda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin" >> /home/user3/.profile  && \
    mkdir -p /home/user3/.local/share/jupyter/kernels/ir  && \
    cp /root/.local/share/jupyter/kernels/ir/* /home/user3/.local/share/jupyter/kernels/ir/  && \
    chown -R user3:user3 /home/user3

## Start jupyterhub using config file
CMD ["jupyterhub","-f","/srv/jupyterhub/jupyterhub_config.py"]