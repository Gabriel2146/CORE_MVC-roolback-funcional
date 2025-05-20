import { mount } from '@vue/test-utils'
import AnalysisDashboard from '../AnalysisDashboard.vue'
import axios from 'axios'

jest.mock('axios')

describe('AnalysisDashboard.vue', () => {
  let wrapper

  beforeEach(async () => {
    axios.get.mockImplementation(url => {
      if (url.endsWith('/api/users/')) {
        return Promise.resolve({ data: [{ id: 1, username: 'athlete1' }, { id: 2, username: 'athlete2' }] })
      }
      if (url.includes('/api/training-plans/')) {
        return Promise.resolve({
          data: [
            {
              id: 1,
              sessions: [
                { date: '2023-01-01', exercise_entries: [1, 2] },
                { date: '2023-01-02', exercise_entries: [3] }
              ]
            }
          ]
        })
      }
      return Promise.resolve({ data: [] })
    })

    wrapper = mount(AnalysisDashboard)
    await wrapper.vm.$nextTick()
  })

  it('renders athlete filter options', () => {
    const options = wrapper.findAll('option')
    expect(options).toHaveLength(2)
    expect(options[0].text()).toBe('athlete1')
    expect(options[1].text()).toBe('athlete2')
  })

  it('fetches and renders progress data on athlete change', async () => {
    wrapper.vm.selectedAthlete = 2
    await wrapper.vm.$nextTick()
    expect(axios.get).toHaveBeenCalledWith('http://localhost:8000/api/training-plans/?user=2')
  })
})
