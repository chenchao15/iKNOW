<template>
  <div class="other-tutorial">
    <div v-for="(i, index) in info" :key="i.id">
      <Card style="width:600px;margin-bottom: 10px">
        <a @click="clickDetail(i.id)"><h3 style="word-break:break-all; word-wrap:break-word">{{i.title}}</h3></a>
        <p class="layout-group-p" v-if="type === 0"><strong>作者: </strong>{{i.author.contestant_user.name}}</p>
        <p class="layout-group-p" v-else-if="type === 1"><strong>作者: </strong>{{i.author.organizer_user.name}}</p>
        <p class="layout-group-p"><strong>发布时间: </strong>{{i.post_time}}</p>
      </Card>
    </div>
  </div>
</template>

<script>
export default {
  name: 'other',
  props: ['id', 'type'],
  data () {
    return {
      info: {}
    }
  },
  created () {
    this.links()
  },
  methods: {
    links () {
      var res
      if (this.type === 0) {
        this.$http.get(this.GLOBAL.baseUrl + 'api/userpage/other_contestant_tutorial?id=' + this.id)
          .then((response) => {
            res = JSON.parse(response.bodyText)
            this.info = res
          })
          .catch((response) => {
            this.$Message.error('获取教程信息失败')
          })
      } else {
        this.$http.get(this.GLOBAL.baseUrl + 'api/userpage/other_organizer_tutorial?id=' + this.id)
          .then((response) => {
            res = JSON.parse(response.bodyText)
            this.info = res
          })
          .catch((response) => {
            this.$Message.error('获取教程信息失败')
          })
      }
    },
    clickDetail (id) {
      this.$router.push('/tutorialDetails/' + id)
    }
  }
}
</script>

<style>
    .other-tutorial{
        margin: 10px 80px;
    }
</style>
