module.exports = {

  apps : [
    {
      script: 'server.py',
      interpreter: '/home/deploy/apps/goods_hunter/venv/bin/python',
    },
    // {
    //   script: 'ghback/manage.py',
    //   args: 'runserver',
    //   interpreter: '/home/deploy/apps/goods_hunter/venv/bin/python',
    // },
    // {
    //   script: 'bot.py',
    //   interpreter: '/home/deploy/apps/goods_hunter/botvenv/bin/python',
    // },
  ],

  deploy : {
    production : {
      user : 'deploy',
      host : '109.196.164.236',
      ref  : 'origin/upgrade',
      repo : 'git@github.com:Vladislavbro/goods_hunter.git',
      path : '/home/deploy/apps/goods_hunter',
      // 'pre-deploy-local': '',
      // 'post-deploy' : 'cd frontend && npm install && npm run build && cd .. && pm2 reload ecosystem.config.js --env production',
      // 'pre-setup': ''
    }
  }
};
