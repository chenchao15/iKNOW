<template>
<div>
  <navigationBar></navigationBar>
  <div class="layout">
    <div class="layout-content">
      <div class="layout-content-title">
        <p class="tutorial-title">发布新教程</p>
        <hr color="#bbbec4" size="2" />
　　　　　　　　<div class="layout-content-main">
　　　　　　　　　　<Form ref="currentShare" :model="currentShare" label-width="50" style="font-weight:bold">
            <FormItem label="题目" prop="title">
              <Input v-model="currentShare.title"></Input>
            </FormItem>
            <FormItem label="简介" prop="brief">
              <Input v-model="currentShare.brief"></Input>
            </FormItem>
            <Upload
               class="tutorial-pic"
              :on-success="handleSuccess"
              :show-upload-list="false"
              :format="['jpg','jpeg','png','bmp']"
              :on-format-error="handleFormatError"
              :action="this.GLOBAL.baseUrl + 'api/tutorial/image_upload'"
              :headers="{
                'X-CSRFToken':cookie
              }">
              <Button type="dashed" style="font-size: 16px">在正文中插入图片</Button>
            </Upload>
            <FormItem label="正文" prop="content">
              <Input v-model="currentShare.content" type="textarea" :autosize="{minRows: 15,maxRows: 50}"></Input>
            </FormItem>
          </Form>
          <Button style="margin-left: 800px" type="primary" size="large" @click="handleTutarial(0)">暂存</Button>
　　　　　　　　　　<Button style="margin-left: 20px" type="success" size="large" @click="handleTutarial(1)">发布</Button>
        </div>
      </div>
    </div>
    <div class="layout-copy">
      2011-2017 &copy; iKNOW
    </div>
  </div>
</div>
</template>

<script>
import navigationBar from '../components/navigationBar'
export default {
  name: 'StudentShare',
  data () {
    return {
      chooseTheme: 'light',
      cookie: this.getCookie('csrftoken'),
      currentShare: {
        title: '',
        content: '',
        author: {
          id: 1,
          name: 'fddf',
          avatar_url: ''
        },
        brief: '',
        createTime: '',
        id: -1
      }
    }
  },
  components: {
    navigationBar
  },
  watch: {
    '$route' (to, from) {
      if (to.path === '/createtutorial') {
        this.currentShare.title = ''
        this.currentShare.content = ''
        this.currentShare.brief = ''
      }
    }
  },
  methods: {
    getCookie (name) {
      let reg = new RegExp('(^| )' + name + '=([^;]*)(;|$)')
      let arr
      if ((arr = document.cookie.match(reg))) {
        return decodeURIComponent(arr[2])
      }
    },
    goShare () {
      this.shareModal = true
    },
    checkInput () {
      if (this.currentShare.title === '' || this.currentShare.brief === '' || this.currentShare.content === '') {
        return false
      } else {
        return true
      }
    },
    handleFormatError (file) {
      this.$Notice.warning({
        title: '文件类型错误',
        desc: '文件' + file.name + '的格式或类型不正确, 请上传图片格式文件(jpg,jpeg,png or bmp).'
      })
    },
    handleSuccess (res, file) {
      var picString = '\n<img src="' + res.image_url + '" width="600px" height="400px" style="text-align:center"/>'
      this.currentShare.content += picString
    },
    handleTutarial (status) {
      if (this.checkInput() || status === 0) {
        var dataPost = {
          status: status,
          title: this.currentShare.title,
          brief: this.currentShare.brief,
          content: ''
        }
        for (var i = 0; i < this.currentShare.content.length; i++) {
          if (this.currentShare.content[i] === '\n') {
            dataPost.content += '<br/>'
          } else {
            dataPost.content += this.currentShare.content[i]
          }
        }
        this.$http.post(this.GLOBAL.baseUrl + 'api/tutorial/post_tutorial', dataPost)
        .then((response) => {
          if (status === 0) {
            this.$Message.success('暂存成功')
          } else if (status === 1) {
            this.$Message.success('发布成功')
          }
        })
        .catch((response) => {
          if (status === 0) {
            this.$Message.error('暂存失败')
          } else if (status === 1) {
            this.$Message.success('发布失败')
          }
        })
      } else {
        this.$Message.error('您填写的信息不完整')
      }
    }
  }
}
</script>

<style scoped>
    .tutorial-title{
        margin: 10px;
        text-align: center;
        display: inline-block;
        font-size: 25px;
        color: #666;
        font-weight: 600;
        overflow: hidden;
    }
    .share-button{
        margin: 10px;
        margin-left: 80px;
        text-align:center;
        display: inline-block;
        font-family: "PingFang SC";
        font-size: 18px;
        overflow: hidden;
    }
    .tutorial-content{
        margin: 20px 50px;
        z-index: 0;
    }
    .tutorial-tabpane{
        margin-top: -15px;
        padding: 0px 60px;
    }
    .layout{
        border: 1px solid #d7dde4;
        background: #f5f7f9;
    }
    .layout-logo{
        width: 100px;
        height: 30px;
        background: #5b6270;
        border-radius: 3px;
        float: left;
        position: relative;
        top: 15px;
        left: 20px;
    }
    .layout-nav{
        width: 420px;
        margin: 0 auto;
    }
    .layout-assistant{
        width: 300px;
        margin: 0 auto;
        height: inherit;
    }
    .layout-breadcrumb{
        padding: 10px 15px 0;
    }
    .layout-content{
        min-height: 200px;
        margin: 15px;
        padding: 50px;
        padding-top: 10px;
        overflow: hidden;
        background: #fff;
        border-radius: 4px;
    }
    .layout-content-title{
        padding: 10px;
    }
    .layout-content-main{
        padding: 30px 30px 30px 10px;
    }
    .layout-copy{
        text-align: center;
        padding: 10px 0 20px;
        color: #9ea7b4;
    }
    .forum-modal{
        margin: 10px 30px 20px 30px;
        text-align: center;
    }
    .tutorial-pic{
        margin-left: 810px;
        margin-bottom: 10px;
    }
</style>
