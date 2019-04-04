<template>
  <div>
    <Table border :columns="columns" :data="datas"></Table>
  </div>
</template>
<script>

export default {
  name: 'leaderBoard',
  props: ['stageId'],
  data () {
    return {
      columns: [
        {
          title: '排名',
          type: 'index',
          width: 80,
          align: 'center'
        },
        {
          title: '姓名',
          key: 'name',
          align: 'center',
          render: (h, params) => {
            return h('div', this.datas[params.index].contestant.name)
          }
        },
        {
          title: '得分',
          key: 'submit_grade',
          align: 'center',
          ellipsis: 'true'
        }
      ],
      datas: [
      ]
    }
  },
  mounted () {
    this.$http.get(this.GLOBAL.baseUrl + 'api/competition/leader_board', {params: { phase_id: this.stageId }})
    .then((response) => {
      var res = JSON.parse(response.bodyText)
      this.datas = res
    })
    .catch((response) => {
      this.$Message.error('获取排行榜失败')
      this.datas = []
    })
  },
  methods: {
  }
}
</script>
<style scoped>
</style>