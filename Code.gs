function onHomepage(e) {
  var card = CardService.newCardBuilder();
  card.setHeader(CardService.newCardHeader().setTitle("AI Label Assistant"));
  
  var section = CardService.newCardSection();
  section.addWidget(CardService.newTextButton()
    .setText("Create New AI Label")
    .setOnClickAction(CardService.newAction().setFunctionName("createNewAILabel")));
  
  card.addSection(section);
  
  return card.build();
}

function createNewAILabel(e) {
  var aiAutomation = e && e.formInput ? e.formInput.aiAutomation : 'false';
  
  var card = CardService.newCardBuilder();
  card.setHeader(CardService.newCardHeader().setTitle("Create New AI Label"));
  
  var section = CardService.newCardSection();
  section.addWidget(CardService.newTextInput()
    .setFieldName("labelName")
    .setTitle("Label Name"));
  
  section.addWidget(CardService.newSelectionInput()
    .setFieldName("aiAutomation")
    .setTitle("AI Automation")
    .setType(CardService.SelectionInputType.DROPDOWN)
    .addItem("Disabled", "false", aiAutomation === 'false')
    .addItem("Enabled", "true", aiAutomation === 'true')
    .setOnChangeAction(CardService.newAction().setFunctionName("updateAIAutomation")));
  
  if (aiAutomation === 'true') {
    section.addWidget(CardService.newTextInput()
      .setFieldName("rule")
      .setTitle("Rule")
      .setHint("Enter your rule here"));
  }
  
  section.addWidget(CardService.newTextButton()
    .setText("Create Label")
    .setOnClickAction(CardService.newAction().setFunctionName("saveLabel")));
  
  card.addSection(section);
  
  return card.build();
}

function updateAIAutomation(e) {
  var aiAutomation = e.formInput.aiAutomation;
  return CardService.newActionResponseBuilder()
    .setNavigation(CardService.newNavigation()
      .updateCard(createNewAILabel(e)))
    .build();
}

function saveLabel(e) {
  var labelName = e.formInput.labelName;
  var aiAutomation = e.formInput.aiAutomation;
  var rule = e.formInput.rule;
  
  if (!labelName) {
    return CardService.newActionResponseBuilder()
      .setNotification(CardService.newNotification()
        .setText("Please enter a label name"))
      .build();
  }

  if (!aiAutomation) {
    return CardService.newActionResponseBuilder()
      .setNavigation(CardService.newNavigation()
        .updateCard(createNewAILabel(e)))
      .setNotification(CardService.newNotification()
        .setText("Please select either Disabled or Enabled for AI Automation"))
      .build();
  }

  if (aiAutomation === "true" && (!rule || rule.trim() === "")) {
    return CardService.newActionResponseBuilder()
      .setNavigation(CardService.newNavigation()
        .updateCard(createNewAILabel(e)))
      .setNotification(CardService.newNotification()
        .setText("Please enter a rule for AI Automation"))
      .build();
  }
  
  try {
    var label = GmailApp.createLabel(labelName);
    
    if (aiAutomation === "true") {
      var userProperties = PropertiesService.getUserProperties();
      var rules = JSON.parse(userProperties.getProperty('aiRules') || '{}');
      rules[labelName] = rule;
      userProperties.setProperty('aiRules', JSON.stringify(rules));
    }
    
    return CardService.newActionResponseBuilder()
      .setNotification(CardService.newNotification()
        .setText("Label created successfully: " + labelName))
      .build();
  } catch (error) {
    return CardService.newActionResponseBuilder()
      .setNotification(CardService.newNotification()
        .setText("Error creating label: " + error.toString()))
      .build();
  }
}


function storeRule(labelName, rule) {
  var userProperties = PropertiesService.getUserProperties();
  var rules = JSON.parse(userProperties.getProperty('aiRules') || '{}');
  rules[labelName] = rule;
  userProperties.setProperty('aiRules', JSON.stringify(rules));
}

function getRules() {
  var userProperties = PropertiesService.getUserProperties();
  return JSON.parse(userProperties.getProperty('aiRules') || '{}');
}

function onGmailMessage(e) {
  return CardService.newCardBuilder().build();
}