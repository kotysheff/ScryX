import QtQuick
import QtQuick.Controls
import QtQuick.Effects
import QtQuick.Particles

Window {
    id: root
    width: 1000
    height: 700
    visible: true
    title: "PySide6 Ultra Liquid Engine"
    color: "#05050c"

    Item {
        id: fluidBackground
        anchors.fill: parent

        ParticleSystem { id: particleSystem }

        Emitter {
            system: particleSystem
            emitRate: 40
            lifeSpan: 4000
            size: 180
            sizeVariation: 50
            anchors.fill: parent
            velocity: AngleDirection { angle: 45; angleVariation: 360; magnitude: 30 }
        }

        Emitter {
            system: particleSystem
            emitRate: 60
            lifeSpan: 1500
            size: 40
            x: mouseTracker.mouseX
            y: mouseTracker.mouseY
            velocity: AngleDirection { angle: 0; angleVariation: 360; magnitude: 40 }
        }

        ImageParticle {
            system: particleSystem
            source: "qrc:///particleresources/glowdot.png"
            color: "#6c5ce7"
            colorVariation: 0.4
            alpha: 0.15
        }

        MouseArea {
            id: mouseTracker
            anchors.fill: parent
            hoverEnabled: true
        }
    }

    Item {
        id: glassCard
        width: 600
        height: 450
        anchors.centerIn: parent

        Rectangle {
            id: cardBase
            anchors.fill: parent
            radius: 32
            color: "transparent"

            MouseArea {
                id: mouseZone
                anchors.fill: parent
                hoverEnabled: true
            }
        }

        MultiEffect {
            source: fluidBackground
            anchors.fill: cardBase
            blurEnabled: true
            blur: 1.0
            shadowEnabled: true
            shadowColor: "#000000"
            shadowOpacity: 0.7
            shadowBlur: 1.0
            shadowVerticalOffset: 25

            maskEnabled: true
            maskSource: ShaderEffectSource {
                sourceItem: Rectangle {
                    width: cardBase.width; height: cardBase.height; radius: cardBase.radius
                }
            }
        }

        Rectangle {
            anchors.fill: parent; radius: 32; border.width: 1
            border.color: "white"; opacity: 0.12; color: "#08ffffff"
        }

        Column {
            anchors.fill: parent
            anchors.margins: 45
            spacing: 25

            Row {
                width: parent.width
                spacing: 15
                Text {
                    text: "QUANTUM CORE"
                    color: "#ffffff"
                    font.pixelSize: 26; font.bold: true; font.letterSpacing: 3
                }

                Rectangle {
                    height: 25; width: 110; radius: 6
                    color: Backend.get_status() === "PROCESSING" ? "#ffb142" :
                           Backend.get_status() === "COMPLETED" ? "#2ed573" : "#1e90ff"

                    Text {
                        anchors.centerIn: parent
                        text: Backend.get_status()
                        color: "white"; font.pixelSize: 11; font.bold: true
                    }
                }
            }

            Rectangle {
                width: parent.width; height: 100
                color: "#15000000"
                radius: 12; border.width: 1; border.color: "#15ffffff"
                clip: true

                Text {
                    id: logText
                    anchors.centerIn: parent
                    text: Backend.get_log()
                    color: "#00cec9"
                    font.family: "Consolas"
                    font.pixelSize: 15

                    Behavior on text {
                        SequentialAnimation {
                            NumberAnimation { target: logText; property: "opacity"; to: 0; duration: 50 }
                            NumberAnimation { target: logText; property: "opacity"; to: 1; duration: 100 }
                        }
                    }
                }
            }

            Column {
                width: parent.width
                spacing: 8
                Text { text: "MATRIX COMPILATION PROGRESS"; color: "#a4b0be"; font.pixelSize: 11; font.bold: true }

                ProgressBar {
                    id: controlProgress
                    width: parent.width
                    value: Backend.get_progress()

                    background: Rectangle { implicitHeight: 6; color: "#20ffffff"; radius: 3 }
                    contentItem: Item {
                        Rectangle {
                            width: controlProgress.visualPosition * parent.width; height: 6
                            radius: 3
                            gradient: Gradient {
                                GradientStop { position: 0.0; color: "#6c5ce7" }
                                GradientStop { position: 1.0; color: "#00cec9" }
                            }
                        }
                    }
                    Behavior on value { NumberAnimation { duration: 100 } }
                }
            }

            Button {
                id: actionButton
                enabled: Backend.get_status() !== "PROCESSING"
                text: Backend.get_status() === "PROCESSING" ? "COMPUTING..." : "INITIALIZE CORE"

                onClicked: Backend.start_matrix_computation()

                contentItem: Text {
                    text: actionButton.text
                    font.pixelSize: 13; font.bold: true; color: "white"
                    horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter
                }

                background: Rectangle {
                    implicitWidth: 180; implicitHeight: 48; radius: 14
                    color: actionButton.enabled ? (actionButton.hovered ? "#00cec9" : "#6c5ce7") : "#2d3436"
                    Behavior on color { ColorAnimation { duration: 250 } }
                }
                scale: actionButton.pressed ? 0.96 : 1.0
                Behavior on scale { NumberAnimation { duration: 100 } }
            }
        }

        transform: [
            Rotation {
                angle: (mouseZone.mouseX - glassCard.width/2) * 0.02
                axis { x: 0; y: 1; z: 0 }
                origin.x: glassCard.width/2; origin.y: glassCard.height/2
            },
            Rotation {
                angle: -(mouseZone.mouseY - glassCard.height/2) * 0.03
                axis { x: 1; y: 0; z: 0 }
                origin.x: glassCard.width/2; origin.y: glassCard.height/2
            }
        ]
        Behavior on transform {
            enabled: !mouseZone.containsMouse
            PropertyAnimation { duration: 600; easing.type: Easing.OutElastic; easing.amplitude: 1.0 }
        }
    }
}
