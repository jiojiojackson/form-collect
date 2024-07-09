const { defineConfig } = require('@vue/cli-service')
const dotenv = require('dotenv')

// 加载环境变量
dotenv.config()

module.exports = defineConfig({
  transpileDependencies: true
})
