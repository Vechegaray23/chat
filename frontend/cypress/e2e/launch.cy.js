describe('Survey upload', () => {
  it('uploads valid survey', () => {
    cy.visit('/')
    cy.get('input[type=file]').selectFile('cypress/fixtures/survey.json')
    cy.contains('Upload').click()
    cy.contains('Link').should('exist')
  })

  it('shows error on invalid survey', () => {
    cy.visit('/')
    cy.get('input[type=file]').selectFile('cypress/fixtures/bad.json')
    cy.contains('Upload').click()
    cy.contains('error', { matchCase: false })
  })
})
