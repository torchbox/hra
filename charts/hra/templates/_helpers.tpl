{{- define "environment" }}
envFrom: 
- configMapRef:
    name: {{ .Release.Name }}
env:
- name: DATABASE_PASSWORD
    valueFrom:
    secretKeyRef:
        name: {{ .Release.Name }}
        key: DatabasePassword
- name: CFG_EMAIL_HOST_PASSWORD
    valueFrom:
    secretKeyRef:
        name: backing-services
        key: SmtpPassword
- name: ES_SECRET_ACCESS_KEY
    valueFrom:
    secretKeyRef:
        name: backing-services
        key: ElasticSearchSecretAccessKey
- name: RECAPTCHA_PRIVATE_KEY
    valueFrom:
    secretKeyRef:
        name: {{ .Release.Name }}
        key: RecaptchaPrivateKey
- name: HARP_API_PASSWORD
    valueFrom:
    secretKeyRef:
        name: {{ .Release.Name }}
        key: HarpApiPassword
{{- end }}