<template>
  <div class="collectTutorial">
    <Row v-for="tutorial in tutorials" :key="tutorial.id">
      <Card style="margin-top:25px;width:600px;height:150px;" @click="checkAllTutorial">
        <Col span="12">
          <h2 style="text-align:center">{{tutorial.title}}</h2>
          <p v-if="tutorial.author.contestant_user !== null" style="margin-left:40px;margin-top:5px;font-size:14px;color:#657180">发布者: {{tutorial.author.contestant_user.name}}</p>
          <p v-if="tutorial.author.organizer_user !== null" style="margin-left:40px;margin-top:5px;font-size:14px;color:#657180">发布者: {{tutorial.author.organizer_user.name}}</p>
          <p style="margin-left:40px;font-size:14px;color:#657180">发布时间: {{tutorial.post_time}}</p>
        </Col>
        <Col span="12">
          <Button style="margin-top:5px;margin-left:60px" type="warning" @click="checkAllTutorial(tutorial.id)" size="small">取消收藏</Button>
          <Button style="margin-top:5px;margin-left:10px" type="info" @click="checkAllTutorial(tutorial.id)" size="small">点击查看教程详情</Button>
          <p style="margin-left:20px;margin-top:10px;font-size:12px;color:#9ea7b4">教程简介: {{tutorial.brief}}</p>
        </Col>
      </Card>
    </Row>
  </div>
</template>

<script>
export default {
  name: 'collectTutorial',
  data () {
    return {
      tutorials: []
    }
  },
  mounted () {
    this.links()
  },
  methods: {
    links () {
      var dataGet = {
        status: 2
      }
      this.$http.get(this.GLOBAL.baseUrl + 'api/tutorial/tutorial', {params: dataGet})
      .then((response) => {
        var res = JSON.parse(response.bodyText)
        this.tutorials = res.tutorials
      })
      .catch((response) => {
        this.$Message.error('获取收藏教程失败')
      })
    },
    checkAllTutorial (id) {
      var dataPost = {
        tutorial_id: id,
        status: 0
      }
      this.$http.post(this.GLOBAL.baseUrl + 'api/userpage/collect_tutorial', dataPost)
      .then((response) => {
        this.$Message.success('取消收藏教程成功')
        this.links()
      })
      .catch((response) => {
        this.$Message.error('取消收藏教程失败')
      })
    }
  }
}
</script>

<style>
    .ivu-card-body{
        padding: 7px;
    }
    .icon{
        position: relative;
        left: 240px;
    }
</style>
