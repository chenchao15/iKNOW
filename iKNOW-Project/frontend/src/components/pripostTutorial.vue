<template>
  <div class="postTutorial">
    <Row v-for="tutorial in tutorials" :key="tutorial.id">
      <Card style="margin-top:25px;width:600px;height:150px;" @click="checkAllTutorial">
        <Col span="12">
          <h2 style="text-align:center">{{tutorial.title}}</h2>
          <p style="margin-left:40px;font-size:14px;color:#657180">发布时间: {{tutorial.post_time}}</p>
        </Col>
        <Col span="12">
          <Button style="margin-top:5px;margin-left:60px" type="warning" @click="deleteTutorial(tutorial.id)" size="small">删除教程</Button>
          <Button style="margin-top:5px;margin-left:10px" type="info" @click="checkAllTutorial(tutorial.id)" size="small">点击查看教程详情</Button>
          <p style="margin-left:20px;margin-top:10px;font-size:12px;color:#9ea7b4">教程简介: {{tutorial.brief}}</p>
        </Col>
      </Card>
    </Row>
  </div>
</template>

<script>
export default {
  name: 'postTutorial',
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
        status: 1
      }
      this.$http.get(this.GLOBAL.baseUrl + 'api/tutorial/tutorial', {params: dataGet})
      .then((response) => {
        var res = JSON.parse(response.bodyText)
        this.tutorials = res.tutorials
      })
      .catch((response) => {
        this.$Message.error('获取已发布教程失败')
      })
    },
    deleteTutorial (id) {
      this.$http.delete(this.GLOBAL.baseUrl + 'api/tutorial/tutorial_info/' + id)
      .then((response) => {
        this.links()
        this.$Message.success('删除教程成功')
      })
      .catch((response) => {
        this.$Message.error('删除教程失败')
      })
    },
    checkAllTutorial (id) {
      this.$router.push('/tutorialDetails/' + id)
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
