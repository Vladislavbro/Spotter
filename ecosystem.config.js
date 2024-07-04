module.exports = {

  apps : [
    // {
    //   script: 'e.py',
    //   interpreter: '/home/deploy/apps/goods_hunter/venv/bin/python',
    // },
    {
      interpreter: '/usr/bin/node',
      script: 'front-site/.output/server/index.mjs'
    },
    {
      script: 'ghback/manage.py',
      args: 'runserver',
      interpreter: '/home/deploy/venv/bin/python',
    },
    // {
    //   script: 'bot.py',
    //   interpreter: '/home/deploy/apps/goods_hunter/botvenv/bin/python',
    // },
  ],

  deploy : {
    production : {
      user : 'deploy',
      host : '194.87.101.169',
      ref  : 'origin/upgrade',
      repo : 'git@github.com:Vladislavbro/goods_hunter.git',
      path : '/home/deploy/apps/spotter',
      // 'pre-deploy-local': '',
      'post-deploy' : 'cd front-site && \
                      yarn install && \
                      yarn build && \
                      cd .. && \
                      pm2 reload ecosystem.config.js --env production',
      // 'pre-setup': ''
    }
  }
};
