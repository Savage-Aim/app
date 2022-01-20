import Vue from 'vue'
import Vuex, { ActionTree, MutationTree } from 'vuex'
import { Character } from './interfaces/character'
import Gear from './interfaces/gear'
import Job from './interfaces/job'
import Team from './interfaces/team'
import Tier from './interfaces/tier'
import User from './interfaces/user'

Vue.use(Vuex)

interface State {
  characters: Character[],
  gear: Gear[],
  jobs: Job[],
  maxItemLevel: number
  minItemLevel: number
  teams: Team[],
  tiers: Tier[],
  user: User,
  version: string,
}

interface Store {
  actions: ActionTree<unknown, unknown>,
  mutations: MutationTree<State>,
  state: State,
}

const DEFAULT_USER = {
  avatar_url: '',
  id: null,
  theme: 'beta',
  username: '',
}

const store: Store = {
  actions: {
    async fetchCharacters({ commit }): Promise<void> {
      try {
        const response = await fetch(`/backend/api/character/`)
        if (response.ok) {
          // Parse the list into an array of character interfaces and store them in the character data list
          commit('setCharacters', await response.json() as Character[])
        }
        else if (response.status !== 403) {
          Vue.notify({ text: `Error ${response.status} when fetching Characters.`, type: 'is-danger' })
        }
      }
      catch (e) {
        Vue.notify({ text: `Error ${e} when fetching Characters.`, type: 'is-danger' })
      }
    },

    async fetchGear({ commit }): Promise<void> {
      try {
        const response = await fetch(`/backend/api/gear/`)
        if (!response.ok) {
          Vue.notify({ text: `Error ${response.status} when fetching Gear list.`, type: 'is-danger' })
        }
        else {
          commit('setGear', await response.json() as Gear[])
        }
      }
      catch (e) {
        Vue.notify({ text: `Error ${e} when fetching Gear list.`, type: 'is-danger' })
      }
    },

    async fetchItemLevels({ commit }): Promise<void> {
      try {
        const response = await fetch(`/backend/api/gear/item_levels/`)
        if (!response.ok) {
          Vue.notify({ text: `Error ${response.status} when fetching Gear list.`, type: 'is-danger' })
        }
        else {
          const json = await response.json()
          commit('setMaxIL', json.max)
          commit('setMinIL', json.min)
        }
      }
      catch (e) {
        Vue.notify({ text: `Error ${e} when fetching Gear list.`, type: 'is-danger' })
      }
    },

    async fetchJobs({ commit }): Promise<void> {
      try {
        const response = await fetch(`/backend/api/job/`)
        if (!response.ok) {
          Vue.notify({ text: `Error ${response.status} when fetching Jobs list.`, type: 'is-danger' })
        }
        else {
          commit('setJobs', await response.json() as Job[])
        }
      }
      catch (e) {
        Vue.notify({ text: `Error ${e} when fetching Jobs list.`, type: 'is-danger' })
      }
    },

    async fetchTeams({ commit }): Promise<void> {
      // Fetch teams for all characters under the control of the logged in user
      try {
        const response = await fetch(`/backend/api/team/`)
        if (response.ok) {
          // Parse the list into an array of character interfaces and store them in the character data list
          commit('setTeams', await response.json() as Team[])
        }
        else if (response.status !== 403) {
          Vue.notify({ text: `Error ${response.status} when fetching Teams.`, type: 'is-danger' })
        }
      }
      catch (e) {
        Vue.notify({ text: `Error ${e} when fetching Teams.`, type: 'is-danger' })
      }
    },

    async fetchTiers({ commit }): Promise<void> {
      try {
        const response = await fetch(`/backend/api/tier/`)
        if (!response.ok) {
          Vue.notify({ text: `Error ${response.status} when fetching Tiers list.`, type: 'is-danger' })
        }
        else {
          commit('setTiers', await response.json() as Tier[])
        }
      }
      catch (e) {
        Vue.notify({ text: `Error ${e} when fetching Tiers list.`, type: 'is-danger' })
      }
    },

    async fetchUser({ commit, dispatch, state }): Promise<void> {
      try {
        const response = await fetch(`/backend/api/me/`, { credentials: 'include' })
        if (response.ok) {
          // Store the response as the state's user
          commit('setUser', await response.json() as User)

          if ((state as State).user.id !== null) {
            // When mounted, fetch the Character data for the user that is currently logged in
            // We know there is one because this function won't be called unless there is
            dispatch('fetchCharacters')
            // Also fetch team data
            dispatch('fetchTeams')
          }
        }
        else {
          Vue.notify({ text: `Error ${response.status} when fetching User details.`, type: 'is-danger' })
        }
      }
      catch (e) {
        Vue.notify({ text: `Error ${e} when fetching current User.`, type: 'is-danger' })
      }
    },
  },
  mutations: {
    setCharacters(state: State, characters: Character[]) {
      state.characters = characters
    },

    setGear(state: State, gear: Gear[]) {
      state.gear = gear
    },

    setJobs(state: State, jobs: Job[]) {
      state.jobs = jobs
    },

    setMaxIL(state: State, il: number) {
      state.maxItemLevel = il
    },

    setMinIL(state: State, il: number) {
      state.minItemLevel = il
    },

    setTeams(state: State, teams: Team[]) {
      state.teams = teams
    },

    setTheme(state: State, theme: string) {
      state.user.theme = theme
    },

    setTiers(state: State, tiers: Tier[]) {
      state.tiers = tiers
    },

    setUser(state: State, user: User) {
      state.user = user
    },

    resetUser(state: State): void {
      state.user = DEFAULT_USER
    },
  },
  state: {
    characters: [],
    gear: [],
    jobs: [],
    maxItemLevel: 0,
    minItemLevel: 0,
    teams: [],
    tiers: [],
    user: DEFAULT_USER,
    version: process.env.VUE_APP_VERSION,
  },
}

export default new Vuex.Store(store)
