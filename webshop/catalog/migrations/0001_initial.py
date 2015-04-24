# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table('categories', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('meta_keywords', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('meta_description', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['catalog.Category'])),
            (u'lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('catalog', ['Category'])

        # Adding model 'FeelName'
        db.create_table('Feel_product', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('catalog', ['FeelName'])

        # Adding model 'BrandName'
        db.create_table('brand_product', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('catalog', ['BrandName'])

        # Adding model 'Product'
        db.create_table('products', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255)),
            ('brand_name', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.BrandName'], null=True, blank=True)),
            ('not_available', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_bestseller', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_aqua', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_new', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('description', self.gf('ckeditor.fields.RichTextField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('meta_description', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('catalog', ['Product'])

        # Adding M2M table for field categories on 'Product'
        db.create_table('products_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm['catalog.product'], null=False)),
            ('category', models.ForeignKey(orm['catalog.category'], null=False))
        ))
        db.create_unique('products_categories', ['product_id', 'category_id'])

        # Adding M2M table for field feel on 'Product'
        db.create_table('products_feel', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm['catalog.product'], null=False)),
            ('feelname', models.ForeignKey(orm['catalog.feelname'], null=False))
        ))
        db.create_unique('products_feel', ['product_id', 'feelname_id'])

        # Adding M2M table for field itemsAttached on 'Product'
        db.create_table('products_itemsAttached', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_product', models.ForeignKey(orm['catalog.product'], null=False)),
            ('to_product', models.ForeignKey(orm['catalog.product'], null=False))
        ))
        db.create_unique('products_itemsAttached', ['from_product_id', 'to_product_id'])

        # Adding model 'ProductImage'
        db.create_table('product_images', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.Product'])),
            ('default', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('catalog', ['ProductImage'])

        # Adding model 'ProductVolume'
        db.create_table('product_volume', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('volume', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=2)),
            ('weight', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=2)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=2)),
            ('new_price', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=9, decimal_places=2, blank=True)),
            ('default', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.Product'])),
        ))
        db.send_create_signal('catalog', ['ProductVolume'])

        # Adding model 'GiftPrice'
        db.create_table('gift_price', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=2)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('weight', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=2)),
        ))
        db.send_create_signal('catalog', ['GiftPrice'])

        # Adding model 'Cupon'
        db.create_table('catalog_cupon', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('percent', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('catalog', ['Cupon'])

        # Adding model 'Review'
        db.create_table('catalog_review', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('review', self.gf('django.db.models.fields.TextField')()),
            ('photo', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('catalog', ['Review'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table('categories')

        # Deleting model 'FeelName'
        db.delete_table('Feel_product')

        # Deleting model 'BrandName'
        db.delete_table('brand_product')

        # Deleting model 'Product'
        db.delete_table('products')

        # Removing M2M table for field categories on 'Product'
        db.delete_table('products_categories')

        # Removing M2M table for field feel on 'Product'
        db.delete_table('products_feel')

        # Removing M2M table for field itemsAttached on 'Product'
        db.delete_table('products_itemsAttached')

        # Deleting model 'ProductImage'
        db.delete_table('product_images')

        # Deleting model 'ProductVolume'
        db.delete_table('product_volume')

        # Deleting model 'GiftPrice'
        db.delete_table('gift_price')

        # Deleting model 'Cupon'
        db.delete_table('catalog_cupon')

        # Deleting model 'Review'
        db.delete_table('catalog_review')


    models = {
        'catalog.brandname': {
            'Meta': {'object_name': 'BrandName', 'db_table': "'brand_product'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'catalog.category': {
            'Meta': {'ordering': "['-created_at']", 'object_name': 'Category', 'db_table': "'categories'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'meta_description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'meta_keywords': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['catalog.Category']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'catalog.cupon': {
            'Meta': {'object_name': 'Cupon'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'percent': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'catalog.feelname': {
            'Meta': {'object_name': 'FeelName', 'db_table': "'Feel_product'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'catalog.giftprice': {
            'Meta': {'ordering': "['-price']", 'object_name': 'GiftPrice', 'db_table': "'gift_price'"},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '2'}),
            'weight': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '2'})
        },
        'catalog.product': {
            'Meta': {'ordering': "['-created_at']", 'object_name': 'Product', 'db_table': "'products'"},
            'brand_name': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.BrandName']", 'null': 'True', 'blank': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['catalog.Category']", 'symmetrical': 'False'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('ckeditor.fields.RichTextField', [], {}),
            'feel': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['catalog.FeelName']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_aqua': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_bestseller': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_new': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'itemsAttached': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'itemsAttached_rel_+'", 'blank': 'True', 'to': "orm['catalog.Product']"}),
            'meta_description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'not_available': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'catalog.productimage': {
            'Meta': {'object_name': 'ProductImage', 'db_table': "'product_images'"},
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.Product']"})
        },
        'catalog.productvolume': {
            'Meta': {'object_name': 'ProductVolume', 'db_table': "'product_volume'"},
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_price': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '9', 'decimal_places': '2', 'blank': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '2'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.Product']"}),
            'volume': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '2'}),
            'weight': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '2'})
        },
        'catalog.review': {
            'Meta': {'object_name': 'Review'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'photo': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'review': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['catalog']