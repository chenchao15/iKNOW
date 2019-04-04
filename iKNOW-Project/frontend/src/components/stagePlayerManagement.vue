<template>
<div>
  <div v-if="haveDataFlag === true">
    <div v-if="competitionType === 0">
      <stagePersonalCompetition :stageId="stageId"></stagePersonalCompetition>
    </div>
    <div v-else-if="competitionType === 1">
      <stageGroupCompetition :stageId="stageId"></stageGroupCompetition>
    </div>
  </div>
  <div v-else-if="haveDataFlag === false">
    <div class="havedata-div">
      <Button type="dashed" size="large" class="button-import" @click="importData">导入参赛者数据</Button>
    </div>
    <div v-if="importFlag === true" class="candidate-style">
      <candidate v-on:message="recieveMessage" :comId="comId"></candidate>
    </div>
  </div>
</div>
</template>
<script>
  import stagePersonalCompetition from '../components/stagePersonalCompetition'
  import stageGroupCompetition from '../components/stageGroupCompetition'
  import candidate from '../components/candidate'
  export default {
    name: 'stagePlayerManagement',
    props: ['stageId', 'comId'],
    data () {
      return {
        importFlag: false,
        haveDataFlag: false,
        competitionType: null,
        chosenData: null
      }
    },
    components: {
      candidate,
      stagePersonalCompetition,
      stageGroupCompetition
    },
    mounted () {
      this.links()
    },
    methods: {
      links () {
        this.comId = this.$route.params.id
        var dataGet = {
          phase_id: this.stageId
        }
        this.$http.get(this.GLOBAL.baseUrl + 'api/competition/joiner_type', {params: dataGet})
        .then((response) => {
          var res = JSON.parse(response.bodyText)
          this.competitionType = res.joiner_type
          if (res.joiner_number > 0) {
            this.haveDataFlag = true
          }
        })
        .catch((response) => {
          this.$Message.error('获取参赛者类型失败')
          this.competitionType = 0
        })
      },
      importData () {
        if (this.importFlag) {
          this.importFlag = false
        } else {
          this.importFlag = true
        }
      },
      recieveMessage (msg) {
        this.importFlag = false
        this.chosenData = msg
        this.$http.post(this.GLOBAL.baseUrl + 'api/competition/add_joiner', {phase_id: this.stageId, contestant_id: JSON.stringify(this.chosenData)})
          .then((response) => {
            this.$Message.success('导入参赛者信息成功!')
            // this.$router.push('/competitionmanage/' + this.$route.params.id)
          })
          .catch((response) => {
            this.$Message.error('导入参赛者信息失败')
          })
      }
    }
  }
</script>

<style scoped>
  .playermanage-row{
    font-size: 15px;
    margin-top: 10px;
    margin-bottom:10px;
  }
  .havedata-div{
    margin: 50px 0 20px 100px;
    text-align: center;
  }
  .button-import{
    padding: 10px;
    font-size: 25px;
    text-align: center;
  }
  .candidate-style{
    margin-left: 70px;
    margin-bottom: 20px;
    text-align: center;
  }
</style>

