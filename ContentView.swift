import SwiftUI
import OSCKit

protocol Fixture: Identifiable {
    var id: Int { get }
    var color: Color { get set }
}

struct Fixture6CH: Fixture {
    var id: Int
    var color: Color
}

struct Fixture7CH: Fixture {
    var id: Int
    var color: Color
}

struct ContentView: View {
    @State private var selectedFixture = 0
    @State private var fixtures6ch = [
        Fixture6CH(id: 0, color: .white),
        Fixture6CH(id: 1, color: .white),
        Fixture6CH(id: 2, color: .white),
        Fixture6CH(id: 3, color: .white)
    ]
    @State private var fixtures7ch = [
        Fixture7CH(id: 4, color: .white),
        Fixture7CH(id: 5, color: .white),
        Fixture7CH(id: 6, color: .white),
        Fixture7CH(id: 7, color: .white)
    ]
    
    @State private var showSettings = false
    
    private var oscClient = OSCClient()
//    private let remoteHost = "192.168.100.50"
    private let remoteHost = "192.168.0.100"
    private let remotePort: UInt16 = 10000


    var body: some View {
        GeometryReader { geometry in
            ZStack {
                Image(uiImage: UIImage(named: geometry.size.width > geometry.size.height ? "background-horizontal" : "background-vertical")!)
                    .resizable()
                    .edgesIgnoringSafeArea(.all)
                
                VStack {
                    // First row: All, 6-CH, 7-CH
                    HStack {
                        Button(action: {
                            selectedFixture = -1
                        }) {
                            Text("💡🔗💡🔗")
                        }
                        .buttonStyle(SegmentButtonStyle())
                        
                        Button(action: {
                            selectedFixture = -2
                        }) {
                            Text("6-CH")
                        }
                        .buttonStyle(SegmentButtonStyle())
                        
                        Button(action: {
                            selectedFixture = -3
                        }) {
                            Text("7-CH")
                        }
                        .buttonStyle(SegmentButtonStyle())
                    }
                    .padding()
                    
                    // Second row: 6-CH Fixtures
                    HStack {
                        ForEach(0..<4) { index in
                            Button(action: {
                                selectedFixture = index
                            }) {
                                Text("💡 \(index+1)")
                            }
                            .buttonStyle(SegmentButtonStyle())
                        }
                    }
                    .padding()
                    
                    // Third row: 7-CH Fixtures
                    HStack {
                        ForEach(4..<8) { index in
                            Button(action: {
                                selectedFixture = index
                            }) {
                                Text("💡 \(index+1)")
                            }
                            .buttonStyle(SegmentButtonStyle())
                        }
                    }
                    .padding()

                    if selectedFixture >= 0 && selectedFixture < 4 {
                        FixtureControl6CH(fixture: $fixtures6ch[selectedFixture], client: oscClient, host: remoteHost, port: remotePort)
                    } else if selectedFixture >= 4 {
                        FixtureControl7CH(fixture: $fixtures7ch[selectedFixture - 4], client: oscClient, host: remoteHost, port: remotePort)
                    } else if selectedFixture == -1 {
                        AllFixturesControl(fixtures6ch: $fixtures6ch, fixtures7ch: $fixtures7ch, client: oscClient, host: remoteHost, port: remotePort)
                    } else if selectedFixture == -2 {
                        All6CHFixturesControl(fixtures: $fixtures6ch, client: oscClient, host: remoteHost, port: remotePort)
                    } else if selectedFixture == -3 {
                        All7CHFixturesControl(fixtures: $fixtures7ch, client: oscClient, host: remoteHost, port: remotePort)
                    }
                }
                
                VStack {
                    Spacer()
                    HStack {
                        Spacer()
                        Button(action: {
                            showSettings.toggle()
                        }) {
                            Image(systemName: "gearshape")
                                .font(.system(size: 20))
                                .foregroundColor(.black)
                                .padding()
                                .background(
                                    Circle()
                                        .stroke(Color.black, lineWidth: 1)
                                )
                        }
                        .padding()
                        .sheet(isPresented: $showSettings) {
                            SettingsView()
                        }
                    }
                }
            }
        }
        .onAppear {
            do {
                try oscClient.start()
            } catch {
                print("Failed to start OSC Client: \(error)")
            }
        }
        .onDisappear {
            oscClient.stop()
        }
    }
}
struct SegmentButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .padding()
            .background(configuration.isPressed ? Color.gray.opacity(0.5) : Color.gray.opacity(0.2))
            .cornerRadius(10)
            .scaleEffect(configuration.isPressed ? 0.95 : 1.0)
    }
}

struct AllFixturesControl: View {
    @Binding var fixtures6ch: [Fixture6CH]
    @Binding var fixtures7ch: [Fixture7CH]
    var client: OSCClient
    var host: String
    var port: UInt16

    @State private var localColor: Color = .white

    var body: some View {
        VStack {
            ColorPicker("Pick a color for All Fixtures", selection: $localColor)
                .padding()
                .scaleEffect(1.0)
                .onChange(of: localColor) { newColor in
                    fixtures6ch.indices.forEach { fixtures6ch[$0].color = newColor }
                    fixtures7ch.indices.forEach { fixtures7ch[$0].color = newColor }
                    sendColor(newColor)
                }
                .frame(maxWidth: .infinity, alignment: .center) // Center the color picker
        }
        .onAppear {
            if let firstFixtureColor = fixtures6ch.first?.color {
                localColor = firstFixtureColor
            } else if let firstFixtureColor = fixtures7ch.first?.color {
                localColor = firstFixtureColor
            }
        }
    }

    func sendColor(_ color: Color) {
        let rgba = color.toRGBA()
        let allFixtures: [any Fixture] = fixtures6ch + fixtures7ch
        for fixture in allFixtures {
            print("Sending color for fixture \(fixture.id): R=\(rgba.red), G=\(rgba.green), B=\(rgba.blue), A=\(rgba.alpha)")
            let message = OSCMessage(
                OSCAddressPattern("/fixture_all"),
                values: [fixture.id, Int(rgba.red * 255), Int(rgba.green * 255), Int(rgba.blue * 255), Int(rgba.alpha * 255)]
            )
            try? client.send(message, to: host, port: port)
        }
    }
}

struct All6CHFixturesControl: View {
    @Binding var fixtures: [Fixture6CH]
    var client: OSCClient
    var host: String
    var port: UInt16

    @State private var localColor: Color = .white

    var body: some View {
        VStack {
            ColorPicker("Pick a color for 6-CH Fixtures", selection: $localColor)
                .padding()
                .scaleEffect(1.0)
                .onChange(of: localColor) { newColor in
                    fixtures.indices.forEach { fixtures[$0].color = newColor }
                    sendColor(newColor)
                }
                .frame(maxWidth: .infinity, alignment: .center) // Center the color picker
        }
        .onAppear {
            if let firstFixtureColor = fixtures.first?.color {
                localColor = firstFixtureColor
            }
        }
    }

    func sendColor(_ color: Color) {
        let rgba = color.toRGBA()
        for fixture in fixtures {
            print("Sending color for fixture \(fixture.id): R=\(rgba.red), G=\(rgba.green), B=\(rgba.blue), A=\(rgba.alpha)")
            let message = OSCMessage(
                OSCAddressPattern("/fixture_6ch"),
                values: [fixture.id, Int(rgba.red * 255), Int(rgba.green * 255), Int(rgba.blue * 255), Int(rgba.alpha * 255)]
            )
            try? client.send(message, to: host, port: port)
        }
    }
}
struct All7CHFixturesControl: View {
    @Binding var fixtures: [Fixture7CH]
    var client: OSCClient
    var host: String
    var port: UInt16

    @State private var localColor: Color = .white

    var body: some View {
        VStack {
            ColorPicker("Pick a color for 7-CH Fixtures", selection: $localColor)
                .padding()
                .scaleEffect(1.0)
                .onChange(of: localColor) { newColor in
                    fixtures.indices.forEach { fixtures[$0].color = newColor }
                    sendColor(newColor)
                }
                .frame(maxWidth: .infinity, alignment: .center) // Center the color picker
        }
        .onAppear {
            if let firstFixtureColor = fixtures.first?.color {
                localColor = firstFixtureColor
            }
        }
    }

    func sendColor(_ color: Color) {
        let rgba = color.toRGBA()
        for fixture in fixtures {
            print("Sending color for fixture \(fixture.id): R=\(rgba.red), G=\(rgba.green), B=\(rgba.blue), A=\(rgba.alpha)")
            let message = OSCMessage(
                OSCAddressPattern("/fixture_7ch"),
                values: [fixture.id, Int(rgba.red * 255), Int(rgba.green * 255), Int(rgba.blue * 255), Int(rgba.alpha * 255)]
            )
            try? client.send(message, to: host, port: port)
        }
    }
}


struct FixtureControl6CH: View {
      @Binding var fixture: Fixture6CH
      var client: OSCClient
      var host: String
      var port: UInt16

      @State private var localColor: Color

      init(fixture: Binding<Fixture6CH>, client: OSCClient, host: String, port: UInt16) {
          _fixture = fixture
          self.client = client
          self.host = host
          self.port = port
          _localColor = State(initialValue: fixture.wrappedValue.color)
      }

      var body: some View {
          VStack {
              ColorPicker("Pick a color", selection: $localColor)
                  .padding()
                  .scaleEffect(1.0)
                  .onChange(of: localColor) { newColor in
                      fixture.color = newColor
                      sendColor(newColor)
                  }
                  .frame(maxWidth: .infinity, alignment: .center)
          }
          .onChange(of: fixture.color) { newColor in
              localColor = newColor
          }
      }

      func sendColor(_ color: Color) {
          let rgba = color.toRGBA()
          print("Sending color for fixture \(fixture.id): R=\(rgba.red), G=\(rgba.green), B=\(rgba.blue), A=\(rgba.alpha)")
          let message = OSCMessage(
              OSCAddressPattern("/fixture_6ch"),
              values: [fixture.id, Int(rgba.red * 255), Int(rgba.green * 255), Int(rgba.blue * 255), Int(rgba.alpha * 255)]
          )
          try? client.send(message, to: host, port: port)
      }
  }

  struct FixtureControl7CH: View {
      @Binding var fixture: Fixture7CH
      var client: OSCClient
      var host: String
      var port: UInt16

      @State private var localColor: Color

      init(fixture: Binding<Fixture7CH>, client: OSCClient, host: String, port: UInt16) {
          _fixture = fixture
          self.client = client
          self.host = host
          self.port = port
          _localColor = State(initialValue: fixture.wrappedValue.color)
      }

      var body: some View {
          VStack {
              ColorPicker("Pick a color", selection: $localColor)
                  .padding()
                  .scaleEffect(1.0)
                  .onChange(of: localColor) { newColor in
                      fixture.color = newColor
                      sendColor(newColor)
                  }
                  .frame(maxWidth: .infinity, alignment: .center)
          }
          .onChange(of: fixture.color) { newColor in
              localColor = newColor
          }
      }

      func sendColor(_ color: Color) {
          let rgba = color.toRGBA()
          print("Sending color for fixture \(fixture.id): R=\(rgba.red), G=\(rgba.green), B=\(rgba.blue), A=\(rgba.alpha)")
          let message = OSCMessage(
              OSCAddressPattern("/fixture_7ch"),
              values: [fixture.id, Int(rgba.red * 255), Int(rgba.green * 255), Int(rgba.blue * 255), Int(rgba.alpha * 255)]
          )
          try? client.send(message, to: host, port: port)
      }
  }

  struct SettingsView: View {
      @State private var ipAddress: String = "192.168.0.100"
//      @State private var ipAddress: String = "192.168.100.50"

      var body: some View {
          VStack {
              Text("Settings")
                  .font(.largeTitle)
                  .padding()

              HStack {
                  Text("IP Address:")
                  TextField("Enter IP Address", text: $ipAddress)
                      .textFieldStyle(RoundedBorderTextFieldStyle())
                      .padding()
              }
              
              Spacer()
          }
          .padding()
      }
  }

  extension Color {
      func toRGBA() -> (red: Double, green: Double, blue: Double, alpha: Double) {
          let components = self.cgColor?.components ?? [0, 0, 0, 1]
          return (red: Double(components[0]), green: Double(components[1]), blue: Double(components[2]), alpha: Double(components[3]))
      }
  }
