module.exports = {

  apps : [
    {
      script: 'server.py',
      interpreter: '/home/deploy/apps/goods_hunter/venv/bin/python',
    },
    {
      script: 'bot.py',
      interpreter: '/home/deploy/apps/goods_hunter/venv/bin/python',
    },
  ],

  deploy : {
    production_old: {
      user : 'deploy',
      host : '194.87.99.114',
      ref  : 'origin/master',
      repo : 'git@github.com:Vladislavbro/goods_hunter.git',
      path : '/home/deploy/apps/goods_hunter',
    },
    production : {
      user : 'deploy',
      host : '109.196.164.236',
      ref  : 'origin/master',
      repo : 'git@github.com:Vladislavbro/goods_hunter.git',
      path : '/home/deploy/apps/goods_hunter',
      // 'pre-deploy-local': '',
      'post-deploy' : 'cd frontend && npm install && npm run build && cd .. && pm2 reload ecosystem.config.js --env production',
      // 'pre-setup': ''
    }
  }
};
