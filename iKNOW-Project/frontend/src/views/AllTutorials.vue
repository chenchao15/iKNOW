<template>
<div>
  <navigationBar></navigationBar>
  <div class="searchlayout">
    <div class="searchlayout-content">
      <div class="searchlayout-content-main">
        <div v-for="tutorial in eachPageData" :key="tutorial.id">
          <Card class="card-card">
            <Row>
              <Col span="25">
                <Row>
                  <Col span="8">
                    <p class="card-title">
                      {{tutorial.title}}
                    </p>
                  </Col>
                  <Col span="1" offset="13">
                    <Button class="card-buttonone" size="large" type="text" @click="tutorialDetails(tutorial.id)">教程详情<Icon type="forward" size="large"></Icon></Button>
                  </Col>
                </Row>
                <p class="card-p"><span class="card-span">发布组织</span>
                 {{tutorial.author.organizer_user.name}}
                </p>
                <p class="card-p"><span class="card-span">简介</span>
                  {{tutorial.brief}}
                </p>
                <p class="card-p"><span class="card-span">创建时间</span>
                  {{tutorial.post_time}}
                </p>
              </Col>
            </Row>
          </Card>
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
      this.$http.get(this.GLOBAL.baseUrl + 'api/tutorial/offical_tutorial')
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
    changePage (count) {
      this.currentPage = count
      this.links()
    },
    tutorialDetails (id) {
      this.$router.push('/tutorialDetails/' + id)
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
    .searchlayout-page{
        text-align: right;
        padding: 10px 40px 20px;
        
    }
    .searchlayout-copy{
        text-align: center;
        padding: 10px 0 20px;
        color: #9ea7b4;
    }
    .card-card{
        margin: 30px;
    }
    .card-title{
        text-align:center;
        display: inline-block;
        font-size: 18px;
        color: #666;
        line-height: 22px;
        font-weight: 600;
        overflow: hidden;
        text-overflow:ellipsis;
        white-space: nowrap;
    }
    .card-span{
        position: absolute;
        left: 0;
        top: 0;
        color: #aaa;
        font-weight: 600;
    }
    .card-p{
        font-size: 14px;
        color: #aaa;
        line-height: 23px;
        padding-left: 70px;
        position: relative;
    }
    .card-buttonone{
        padding:0;
        font-size: 15px;
    }
</style>
