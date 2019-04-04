<template>
  <div class="saveTutorial">
    <Row v-for="tutorial in tutorials" :key="tutorial.id">
      <Card style="margin-top:25px;width:600px;height:150px;" @click="checkAllTutorial">
        <Col span="12">
          <h2 style="text-align:center">{{tutorial.title}}</h2>
          <p style="margin-left:40px;font-size:14px;color:#657180">发布时间: {{tutorial.post_time}}</p>
        </Col>
        <Col span="12">
          <p style="margin-left:20px;margin-top:10px;font-size:12px;color:#9ea7b4">教程简介: {{tutorial.brief}}</p>
          <Button style="margin-top:5px;margin-left:20px" type="info" @click="postTutorial(tutorial.id)" size="small">发布教程</Button>
          <Button style="margin-top:5px;margin-left:10px" type="warning" @click="deleteTutorial(tutorial.id)" size="small">删除教程</Button>
          <Button style="margin-top:5px;margin-left:10px" type="info" @click="modifyTutorial(tutorial.id)" size="small">修改教程</Button>
        </Col>
      </Card>
    </Row>
  </div>
</template>

<script>
export default {
  name: 'saveTutorial',
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
        status: 0
      }
      this.$http.get(this.GLOBAL.baseUrl + 'api/tutorial/tutorial', {params: dataGet})
      .then((response) => {
        var res = JSON.parse(response.bodyText)
        this.tutorials = res.tutorials
      })
      .catch((response) => {
        this.$Message.error('获取暂存教程失败')
      })
    },
    postTutorial (id) {
      var dataPost = {
        status: 1,
        tutorial_id: id
      }
      this.$http.post(this.GLOBAL.baseUrl + 'api/tutorial/tutorial_status', dataPost)
      .then((response) => {
        this.$Message.success('发布教程成功')
      })
      .catch((response) => {
        this.$Message.error('发布教程失败')
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
    modifyTutorial (id) {
      this.$router.push('/modifyTutorial/' + id)
    }
  }
}
</script>

<style>
    .ivu-card-body{
        padding: 10px;
    }
    .icon{
        position: relative;
        left: 240px;
    }
</style>
