FROM            smallbee3/finn:base
MAINTAINER      smallbee3@gmail.com

ENV         BUILD_MODE production
ENV         DJANGO_SETTINGS_MODULE config.settings.${BUILD_MODE}

# 소스폴더를 통째로 복사
COPY            . /srv/project

# nginx 설정 파일을 복사 및 링크
RUN             cp -f   /srv/project/.config/${BUILD_MODE}/nginx.conf       /etc/nginx/nginx.conf
RUN             cp -f   /srv/project/.config/${BUILD_MODE}/nginx-app.conf  /etc/nginx/sites-available/
RUN             rm -f   /etc/nginx/sites-enalbed/*
RUN             ln -sf  /etc/nginx/sites-available/nginx-app.conf   /etc/nginx/sites-enabled/

# supervisor설정 파일을 복사
RUN             cp -f   /srv/project/.config/${BUILD_MODE}/supervisord.conf  /etc/supervisor/conf.d/

# pkil niginx후 supervisord -n실행
CMD             pkill nginx; supervisord -n
EXPOSE          80