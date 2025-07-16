describe('Survey upload', () => {
  it('uploads valid survey', () => {
    cy.visit('/')
    const file = { fileContent: '{"title":"A","questions":[{"id":"q1","type":"text","text":"ok"}]}', fileName: 'survey.json', mimeType: 'application/json' }
    cy.get('input[type=file]').selectFile(file)
    cy.contains('Upload').click()
    cy.contains('Link').should('exist')
  })

  it('shows error on invalid survey', () => {
    cy.visit('/')
    const file = { fileContent: '{"title":"bad"}', fileName: 'bad.json', mimeType: 'application/json' }
    cy.get('input[type=file]').selectFile(file)
    cy.contains('Upload').click()
    cy.contains('error', { matchCase: false })
  })
})
