<template>
<div>
  <navigationBar></navigationBar>
  <div class="searchlayout">
    <div class="searchlayout-content">
      <div class="searchlayout-content-main">
          <div v-for="(i, index) in eachPageData" :key="i.id">
            <Col span="7" v-if="index % 3 === 0" style="margin-bottom: 15px">
              <Card style="width:320px; background:#dddee1">
                <div style="text-align:center">
                  <a @click="clickDetail(i.id)"><img width="270px" height="150px" :src="i.pic_url"/></a>
                  <h4>{{i.name}}</h4>
                </div>
              </Card>
            </Col>
            <Col span="7" offset="1" v-if="index % 3 !== 0" style="margin-bottom: 15px">
              <Card style="width:320px; background:#dddee1">
                <div style="text-align:center">
                  <a @click="clickDetail(i.id)"><img width="270px" height="150px" :src="i.pic_url"/></a>
                  <h4>{{i.name}}</h4>
                </div>
              </Card>
            </Col>
          </div>
      </div>
    </div>
    <div class="searchlayout-page">
      <Page :total="pageNum" :current="currentPage" @on-change="changePage" show-elevator></Page>    
    </div>
    <div class="searchlayout-copy">
        2011-2017 &copy; iKNOW
    </div>
  </div>
</div>
</template>

<script>
import navigationBar from '../components/navigationBar'
export default {
  name: 'AllCompetitions',
  data () {
    return {
      searchData: [],
      eachPageData: [],
      pageNum: 0,
      currentPage: 1
    }
  },
  components: {
    navigationBar
  },
  mounted () {
    this.currentPage = 1
    this.links()
  },
  methods: {
    links () {
      var res = []
      this.$http.get(this.GLOBAL.baseUrl + 'api/competition/home_competition')
        .then((response) => {
          res = JSON.parse(response.bodyText)
          this.pageNum = (res.length / 6) * 10
          this.searchData = res
          this.getEachPageData()
        })
        .catch((response) => {
          this.$Message.error('抱歉,您还未登录')
        })
    },
    getEachPageData () {
      var index, counts
      var len = this.searchData.length
      this.eachPageData.splice(0, this.eachPageData.length)
      for (index = (this.currentPage - 1) * 6, counts = 0; index < len; index++, counts++) {
        this.eachPageData.push(this.searchData[index])
        if (counts === 5) {
          break
        }
      }
    },
    clickDetail (id) {
      this.$router.push('/competitiondetails/' + id)
    },
    changePage (count) {
      this.currentPage = count
      this.links()
    }
  }
}
</script>

<style>
    .searchlayout{
        border: 1px solid #d7dde4;
        background: #f5f7f9;
    }
    .searchlayout-content{
        min-height: 200px;
        margin: 15px;
        padding: 50px;
        padding-top: 10px;
        padding-bottom:0px;
        overflow: hidden;
        background: #fff;
        border-radius: 4px;
    }
    .searchlayout-content-main{
        padding: 10px;
    }
    .searchlayout-content-p{
        font-size: 15px;
        color: #9ea7b4;
    }
    .searchlayout-page{
        text-align: right;
        padding: 10px 40px 20px;
        
    }
    .searchlayout-copy{
        text-align: center;
        padding: 10px 0 20px;
        color: #9ea7b4;
    }
    .searchlayout-group-p{
        color: #657180;
        margin-left: 20px;
        word-break:break-all;
        word-wrap:break-word;
    }
    .searchlayout-group-img{
        width: 120px;
        height: 120px;
        border-radius: 120px;
        border: 3px solid #f5f7f9;
    }
</style>
