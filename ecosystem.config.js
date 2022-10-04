module.exports = {

  apps : [
    // {
    //   script: 'server.py',
    //   interpreter: '/home/deploy/venv/bin/python',
    // },
  ],

  deploy : {
    production : {
      user : 'deploy',
      host : '194.87.99.114',
      ref  : 'origin/master',
      repo : 'git@github.com:Vladislavbro/goods_hunter.git',
      path : '/home/deploy/apps/goods_hunter',
      // 'pre-deploy-local': '',
      // 'post-deploy' : 'cd frontend && npm install && npm run build && cd .. && pm2 reload ecosystem.config.js --env production',
      // 'pre-setup': ''
    }
  }
};
