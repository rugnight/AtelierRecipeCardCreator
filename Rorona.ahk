#-::
  SetKeyDelay, 10, 50
  Loop 30 {
      Send, {PrintScreen}
      Sleep 1000
      Send j
      Sleep 500
      Send, {PrintScreen}
      Sleep 1000
      Send j
      Sleep 500
      Send {Down}
      Sleep 500
  }

  ;Send, {PrintScreen}
  ;Send, j
  ;Sleep, 100
  ;Send, {PrintScreen}
  ;Sleep, 100
  ;Send, {Down}
  ;Sleep, 100
  Return