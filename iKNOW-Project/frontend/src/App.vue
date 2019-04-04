//整个应用的根组件

<template>
<div class="container" id="app">
  <transition name="fade">
    <keep-alive>
      <router-view></router-view>
    </keep-alive>
  </transition>
</div>
</template>

<script>
export default {
  name: 'app'
}
</script>

<style>
    .container{
        padding-top: 40px;
        width:1170px;
        margin: 0 auto;
        padding-bottom: 20px;
        overflow: hidden;
    }
</style>
