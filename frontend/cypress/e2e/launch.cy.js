describe('Survey upload', () => {
  it('uploads valid survey', () => {
    cy.visit('/')
    cy.get('input[type=file]').selectFile('cypress/fixtures/valid_survey.json')

    cy.contains('Upload').click()
    cy.contains('Link').should('exist')
  })

  it('shows error on invalid survey', () => {
    cy.visit('/')
    const file = { contents: '{"title":"bad"}', fileName: 'bad.json', mimeType: 'application/json' }
    cy.get('input[type=file]').selectFile('cypress/fixtures/invalid_survey.json')
    cy.contains('Upload').click()
    cy.contains('required', { matchCase: false })
  })
})
