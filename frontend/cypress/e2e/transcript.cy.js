describe('Live transcript', () => {
  it('renders partial transcript in real time', () => {
    cy.visit('/', {
      onBeforeLoad(win) {
        class FakeSocket {
          constructor() {
            this.readyState = 1
            setTimeout(() => {
              this.onmessage({ data: JSON.stringify({ transcript: 'hel', confidence: 0.7 }) })
              setTimeout(() => {
                this.onmessage({ data: JSON.stringify({ transcript: 'lo', confidence: 0.9 }) })
              }, 50)
            }, 50)
          }
          send() {}
          close() {}
        }
        win.WebSocket = FakeSocket
      }
    })
    cy.contains('hel')
    cy.contains('hello')
  })
})
