<template>
  <div>
    <BISListDesktopForm
      :bisList="bisList"
      :character="character"
      :errors="errors"
      :displayOffhand="displayOffhand"
      :minIl="minIl"
      :maxIl="maxIl"
      :method="method"
      :url="url"
      v-on:job-change="jobChange"
      v-on:update-min="updateMinIl"
      v-on:update-max="updateMaxIl"
      v-on:error-code="emitErrorCode"
      v-on:errors="handleErrors"
      v-on:save="$emit('save')"
      v-on:close="$emit('close')"
      v-on:import-bis-data="importBISData"
      v-on:import-current-data="importCurrentData"

      v-if="renderDesktop"
    />

    <BISListMobileForm
      :bisList="bisList"
      :character="character"
      :errors="errors"
      :displayOffhand="displayOffhand"
      :minIl="minIl"
      :maxIl="maxIl"
      :method="method"
      :url="url"
      :simpleActions="!renderDesktop"
      v-on:job-change="jobChange"
      v-on:update-min="updateMinIl"
      v-on:update-max="updateMaxIl"
      v-on:error-code="emitErrorCode"
      v-on:errors="handleErrors"
      v-on:save="$emit('save')"
      v-on:close="$emit('close')"
      v-on:import-bis-data="importBISData"
      v-on:import-current-data="importCurrentData"
      :class="[renderDesktop ? 'is-hidden-desktop' : '']"
    />
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'
import BISListDesktopForm from '@/components/bis_list/desktop_form.vue'
import BISListMobileForm from '@/components/bis_list/mobile_form.vue'
import BISListModify from '@/dataclasses/bis_list_modify'
import BISList from '@/interfaces/bis_list'
import { CharacterDetails } from '@/interfaces/character'
import { ImportResponse } from '@/interfaces/imports'
import { BISListErrors } from '@/interfaces/responses'

@Component({
  components: {
    BISListDesktopForm,
    BISListMobileForm,
  },
})
export default class BISListForm extends Vue {
  displayOffhand = true

  @Prop()
  bisList!: BISListModify

  @Prop()
  character!: CharacterDetails

  errors: BISListErrors = {}

  @Prop()
  method!: string

  @Prop({ default: true })
  renderDesktop!: boolean

  @Prop()
  url!: string

  // Set up default values for min and max IL, will change as new tiers are released
  maxIl = 605

  minIl = 580

  jobChange(selectedJob: string): void {
    this.displayOffhand = selectedJob === 'PLD'
  }

  updateMinIl(minIl: number): void {
    this.minIl = minIl
  }

  updateMaxIl(maxIl: number): void {
    this.maxIl = maxIl
  }

  emitErrorCode(errorCode: number): void {
    this.$emit('error-code', errorCode)
  }

  handleErrors(errors: BISListErrors): void {
    this.errors = errors
  }

  importBISData(data: ImportResponse): void {
    if (data.min_il < this.minIl) this.minIl = data.min_il
    if (data.max_il > this.maxIl) this.maxIl = data.max_il
    Vue.nextTick(() => {
      this.bisList.importBIS(data)
      this.jobChange(data.job_id)
      this.$forceUpdate()
      this.$notify({ text: 'Successfully imported BIS Gear!', type: 'is-success' })
    })
  }

  importCurrentData(data: BISList): void {
    // Calculate min and max item levels
    const { minIl, maxIl } = this.calculateCurrentILRange(data)
    if (minIl < this.minIl) this.minIl = minIl
    if (maxIl > this.maxIl) this.maxIl = maxIl
    Vue.nextTick(() => {
      this.bisList.importCurrent(data)
      this.$forceUpdate()
      this.$notify({ text: 'Successfully imported Current Gear!', type: 'is-success' })
    })
  }

  mounted(): void {
    this.displayOffhand = this.bisList.job_id === 'PLD'
  }

  calculateCurrentILRange(data: BISList): { minIl: number, maxIl: number } {
    const itemLevels = [
      data.current_mainhand.item_level,
      data.current_offhand.item_level,
      data.current_head.item_level,
      data.current_body.item_level,
      data.current_hands.item_level,
      data.current_legs.item_level,
      data.current_feet.item_level,
      data.current_earrings.item_level,
      data.current_necklace.item_level,
      data.current_bracelet.item_level,
      data.current_left_ring.item_level,
      data.current_right_ring.item_level,
    ]

    return { minIl: Math.min(...itemLevels), maxIl: Math.max(...itemLevels) }
  }
}
</script>

<style lang="scss">
</style>
