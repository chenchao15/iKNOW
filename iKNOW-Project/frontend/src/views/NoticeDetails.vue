<template>
  <div>
    <navigationBar></navigationBar>
    <div class="layout">
        <div class="layout-content" :key="notice.id">
          <Row>
            <Col span="19">
              <h1>{{notice.title}}</h1>
            </Col>
          </Row>
          <Row>
              <label style="color:#9ea7b4">{{notice.posttime}}</label>
          </Row>
          <hr color="#bbbec4" style="margin: 10px 0"/>
          <p style="font-size:15px" v-html="notice.content"></p>
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
  name: 'NoticeDetails',
  data () {
    return {
      choosetheme: 'light',
      notice: { title: '', author: '', posttime: '', id: 1 }
    }
  },
  components: {
    navigationBar
  },
  mounted () {
    this.$http.get(this.GLOBAL.baseUrl + 'api/competition/notice_detail/' + this.$route.params.id)
    .then((response) => {
      var res = JSON.parse(response.bodyText)
      this.notice = { title: res.title, content: res.content, posttime: '2017.11.23', id: res.id }
    })
  },
  methods: {
  }
}
</script>

<style scoped>
    .layout{
        border: 1px solid #d7dde4;
        background: #f5f7f9;
        margin-top: 2%;
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
        min-height: 100%;
        margin: 15px;
        overflow: hidden;
        background: #fff;
        border-radius: 4px;
        padding:20px;
    }
    .layout-content-main{
        padding: 50px 200px 30px 200px;
    }
    .ivu-col-span-15{
      width: 100%;
    }
    .layout-copy{
        text-align: center;
        padding: 10px 0 20px;
        color: #9ea7b4;
    }
</style>
